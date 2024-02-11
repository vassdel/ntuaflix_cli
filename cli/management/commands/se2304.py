from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError
import json
from cli.models import Movies
from cli.models import Names
from django.core.exceptions import ValidationError
import csv
import requests 
from cli.models import Crews
from cli.models import Episode
from cli.models import Ratings
from cli.models import Principals
from cli.models import Akas
from django.contrib.auth import authenticate
from django.http import JsonResponse

class Command(BaseCommand):
    help = 'Custom Command for our WebApp (Gamo Tin Patra)'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='subcommand')

        # Subparser for the adduser command
        adduser_parser = subparsers.add_parser('adduser')
        adduser_parser.add_argument('--username', required=True)
        adduser_parser.add_argument('--password', required=True)

        # See users in database
        seeusers_parser = subparsers.add_parser('seeusers')

        # Subparser for the login command
        login_parser = subparsers.add_parser('login')
        login_parser.add_argument('--username', required=True)
        login_parser.add_argument('--password', required=True)

        # Subparser for the addmovie command
        addmovie_parser = subparsers.add_parser('addmovie')
        addmovie_parser.add_argument('--tconst', required=True)
        addmovie_parser.add_argument('--titleType', required=True)
        addmovie_parser.add_argument('--primaryTitle', required=True)
        addmovie_parser.add_argument('--originalTitle', required=True)
        addmovie_parser.add_argument('--isAdult', required=True, type=int)
        addmovie_parser.add_argument('--startYear', required=True)
        addmovie_parser.add_argument('--endYear')
        addmovie_parser.add_argument('--runtimeMinutes', type=int)
        addmovie_parser.add_argument('--genres')
        addmovie_parser.add_argument('--img_url_asset')

        #See movies in database
        seeusers_parser = subparsers.add_parser('seemovies')

        # Subparser for the addcrew command
        #addcrew_parser = subparsers.add_parser('addcrew')
        #addcrew_parser.add_argument('--tconst', required=True)
        #addcrew_parser.add_argument('--directors', required=True)
        #addcrew_parser.add_argument('--writers', required=True)

        # New subparser for the newcrew command
        newcrew_parser = subparsers.add_parser('newcrew')
        newcrew_parser.add_argument('--filename', type=str, required=True, help='Path to the TSV file')

        # Subparser for the addepisode command
        addepisode_parser = subparsers.add_parser('addepisode')
        addepisode_parser.add_argument('--tconst', required=True)
        addepisode_parser.add_argument('--parentTconst')
        addepisode_parser.add_argument('--seasonNumber', type=int)
        addepisode_parser.add_argument('--episodeNumber', type=int)

        # Subparser for the addrating command
        addrating_parser = subparsers.add_parser('addrating')
        addrating_parser.add_argument('--tconst', required=True)
        addrating_parser.add_argument('--averageRating', required=True, type=float)
        addrating_parser.add_argument('--numVotes', required=True, type=int)

        # Adding searchtitle subparser
        searchtitle_parser = subparsers.add_parser('searchtitle')
        searchtitle_parser.add_argument('--titlePart', required=True)

        # Adding bygenre subparser
        bygenre_parser = subparsers.add_parser('bygenre')
        bygenre_parser.add_argument('--genre', required=True)
        bygenre_parser.add_argument('--min', type=float, help='Minimum average rating', required=True)
        bygenre_parser.add_argument('--from', dest='yrFrom', type=int, required=False)
        bygenre_parser.add_argument('--to', dest='yrTo', type=int, required=False)

        # Subparser for the addname command
        addname_parser = subparsers.add_parser('addname')
        addname_parser.add_argument('--nameID', required=True)
        addname_parser.add_argument('--name', required=True)
        addname_parser.add_argument('--namePoster')
        addname_parser.add_argument('--birthYear', type=int)
        addname_parser.add_argument('--deathYear', type=int)
        addname_parser.add_argument('--profession')
        addname_parser.add_argument('--titleID')  # Assuming a single title; you could modify this to accept multiple IDs
        addname_parser.add_argument('--category')

        # Subparser for the name command
        name_parser = subparsers.add_parser('name')
        name_parser.add_argument('--nameid', required=True)

        # Subparser for the searchname command
        searchname_parser = subparsers.add_parser('searchname')
        searchname_parser.add_argument('--name', required=True)

        # Inside the add_arguments method, add the following code:
        newepisode_parser = subparsers.add_parser('newepisode')
        newepisode_parser.add_argument('--filename', type=str, required=True, help='Path to the TSV file')

        # Inside the add_arguments method, add the following code:
        newratings_parser = subparsers.add_parser('newratings')
        newratings_parser.add_argument('--filename', type=str, required=True, help='Path to the TSV file')

        newprincipals_parser = subparsers.add_parser('newprincipals')
        newprincipals_parser.add_argument('--filename', type=str, required=True, help='Path to the TSV file')

        newnames_parser = subparsers.add_parser('newnames')
        newnames_parser.add_argument('--filename', type=str, required=True, help='Path to the TSV file')

        newakas_parser = subparsers.add_parser('newakas')
        newakas_parser.add_argument('--filename', type=str, required=True, help='Path to the TSV file')
        
        newtitles_parser = subparsers.add_parser('newtitles')
        newtitles_parser.add_argument('--filename', type=str, required=True, help='Path to the TSV file')



    def handle(self, *args, **options):
        subcommand = options['subcommand'] 
#---------------------------------------------subcommands------------------------------------------------
        if subcommand == 'adduser':
            self.add_user(options['username'], options['password'])
        elif subcommand == 'addmovie':
            self.add_movie(options)
        elif subcommand == 'addcrew':
            self.add_crew(options)
        elif subcommand == 'addepisode':
            self.add_episode(options)
        elif subcommand == 'addrating':
            self.add_rating(options)
        elif subcommand == 'seeusers':
            self.see_users()
        elif subcommand =='seemovies':
            self.see_movies()
        elif subcommand == 'searchtitle':
            self.search_title(options['titlePart'])
        elif subcommand == 'bygenre':
            self.search_by_genre(options['genre'], options.get('yrFrom'), options.get('yrTo'), options.get('min'))
        elif subcommand == 'addname':
            self.add_name(options)
        elif subcommand == 'name':
            self.show_name(options['nameid'])
        elif subcommand == 'searchname':
            self.search_name(options['name'])
        elif subcommand == 'newcrew':
            self.import_crew_from_tsv(options)
        elif subcommand == 'newepisode':
            self.import_episode(options)
        elif subcommand == 'newratings':
            self.import_rating(options)
        elif subcommand == 'newprincipals':
            self.import_principals(options)
        elif subcommand == 'newnames':
            self.import_names(options)
        elif subcommand == 'newakas':
            self.import_akas(options)
        elif subcommand == 'newtitles':
            self.import_titles(options)
        elif subcommand == 'login':
            self.login_user(options)

    def add_user(self, username, password):
        try:
            # Check if the user already exists
            user, created = User.objects.get_or_create(username=username)
            
            # If the user was created, set the password
            if created:
                user.set_password(password)
                user.save()
                message = f"User {username} added successfully."
            else:
                # If the user exists, update the password
                user.set_password(password)
                user.save()
                message = f"User {username}'s password updated successfully."
            
            # Output message
            self.stdout.write(message)

        except Exception as e:
            self.stdout.write(f"An error occurred: {e}")

    def see_users(self):
        users = User.objects.all()
        if users:
            self.stdout.write(f"Total Users: {users.count()}\n")
            for user in users:
                self.stdout.write(f"User ID: {user.id}, Username: {user.username}, Password: {user.password}")
        else:
            self.stdout.write("No users found.")
    
    def add_movie(self, options):

        try:
            # Create a new movie instance and save it to the database
            movie = Movies.objects.create(
                tconst=options['tconst'],
                titleType=options['titleType'],
                primaryTitle=options['primaryTitle'],
                originalTitle=options['originalTitle'],
                isAdult=options['isAdult'],
                startYear=options['startYear'],
                endYear=options.get('endYear'),
                runtimeMinutes=options.get('runtimeMinutes'),
                genres=options.get('genres'),
                img_url_asset=options.get('img_url_asset')
            )

            # Output message
            self.stdout.write(f"Movie {movie.primaryTitle} added successfully.")

        except IntegrityError:
            self.stdout.write(f"A movie with tconst {options['tconst']} already exists.")
        except Exception as e:
            self.stdout.write(f"An error occurred: {e}")

    def see_movies(self):
        movies = Movies.objects.all()
        if movies:
            self.stdout.write(f"Total Movies: {movies.count()}\n")
            for movie in movies:
                self.stdout.write(f"ID: {movie.id}, "
                                  f"Tconst: {movie.tconst}, "
                                  f"Type: {movie.titleType}, "
                                  f"Primary Title: {movie.primaryTitle}, "
                                  f"Original Title: {movie.originalTitle}, "
                                  f"Adult: {'Yes' if movie.isAdult else 'No'}, "
                                  f"Start Year: {movie.startYear}, "
                                  f"End Year: {movie.endYear if movie.endYear else 'N/A'}, "
                                  f"Runtime Minutes: {movie.runtimeMinutes if movie.runtimeMinutes else 'N/A'}, "
                                  f"Genres: {movie.genres if movie.genres else 'N/A'}, "
                                  f"Image URL: {movie.img_url_asset if movie.img_url_asset else 'N/A'}")
        else:
            self.stdout.write("No movies found.")

    def add_crew(self, options):
        # Define the path to your JSON file
        json_file_path = 'crews.json'

        # Open the JSON file and read the data
        try:
            with open(json_file_path, 'r') as file:
                crews = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty/invalid, start with an empty list
            crews = []

        # Append the new crew data
        new_crew = {
            'tconst': options['tconst'],
            'directors': options['directors'],
            'writers': options['writers']
        }
        crews.append(new_crew)

        # Write the updated data back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(crews, file, indent=4)

        # Output message
        self.stdout.write(f"Crew for movie {options['tconst']} added.")
# ok
    def import_crew_from_tsv(self, options):
        tsv_file = options['filename']
        with open(tsv_file, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                tconst = row['tconst']
                directors = row['directors'] if row['directors'] != '\\N' else None
                writers = row['writers'] if row['writers'] != '\\N' else None

                try:
                    crew, created = Crews.objects.update_or_create(
                        tconst=tconst,
                        defaults={
                            'directors': directors,
                            'writers': writers,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created crew entry {crew}'))
                    else:
                        self.stdout.write(f'Updated crew entry {crew}')
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error creating/updating crew entry {tconst}: {e}'))

    def add_episode(self, options):
        # Define the path to your JSON file
        json_file_path = 'episodes.json'

        # Open the JSON file and read the data
        try:
            with open(json_file_path, 'r') as file:
                episodes = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty/invalid, start with an empty list
            episodes = []

        # Append the new episode data
        new_episode = {
            'tconst': options['tconst'],
            'parentTconst': options.get('parentTconst', '\\N'),
            'seasonNumber': options.get('seasonNumber', '\\N'),
            'episodeNumber': options.get('episodeNumber', '\\N')
        }
        episodes.append(new_episode)

        # Write the updated data back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(episodes, file, indent=4)

        # Output message
        self.stdout.write(f"Episode for TV show {options['tconst']} added.")
    
    def add_rating(self, options):
        # Define the path to your JSON file
        json_file_path = 'ratings.json'

        # Open the JSON file and read the data
        try:
            with open(json_file_path, 'r') as file:
                ratings = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty/invalid, start with an empty list
            ratings = []

        # Append the new rating data
        new_rating = {
            'tconst': options['tconst'],
            'averageRating': options['averageRating'],
            'numVotes': options['numVotes']
        }
        ratings.append(new_rating)

        # Write the updated data back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(ratings, file, indent=4)

        # Output message
        self.stdout.write(f"Rating for movie {options['tconst']} added.")
    
    def search_title(self, titlePart):
        # Perform a case-insensitive search for movies with a title containing titlePart
        matching_movies = Movies.objects.filter(originalTitle__icontains=titlePart)
        if matching_movies.exists():
            self.stdout.write(f"Found {matching_movies.count()} movie(s) matching '{titlePart}':")
            for movie in matching_movies:
                self.stdout.write(f"ID: {movie.id}, Title: {movie.originalTitle}")
        else:
            self.stdout.write(f"No movies found matching '{titlePart}'.")

    def search_by_genre(self, genre, yrFrom=None, yrTo=None, min_rating=None):
        # Start with a query for movies matching the genre
        matching_movies = Movies.objects.filter(genres__icontains=genre)

        # Filter by minimum average rating if min_rating is provided
        matching_movies = matching_movies.filter(average_rating__gte=min_rating)

        # Filter by the year range if both yrFrom and yrTo are provided
        if yrFrom is not None and yrTo is not None:
            matching_movies = matching_movies.filter(startYear__gte=yrFrom, startYear__lte=yrTo)

        if matching_movies.exists():
            self.stdout.write(f"Found {matching_movies.count()} movie(s) in genre '{genre}' with a minimum rating of {min_rating}" if min_rating else f"Found {matching_movies.count()} movie(s) in genre '{genre}'")
            if yrFrom and yrTo:
                self.stdout.write(f" within the year range {yrFrom}-{yrTo}:")
            for movie in matching_movies:
                self.stdout.write(f"ID: {movie.id}, Title: {movie.primaryTitle}, Year: {movie.startYear}, Rating: {movie.average_rating}")
        else:
            message = f"No movies found for genre '{genre}'"
            if min_rating:
                message += f" with a minimum rating of {min_rating}"
            if yrFrom and yrTo:
                message += f" within the year range {yrFrom}-{yrTo}."
            self.stdout.write(message)

    """def show_name(self, nameid):
        try:
            # Retrieve the name entry
            name = Name.objects.get(nameID=nameid)
            
            # Output the name attributes
            self.stdout.write(f"Name ID: {name.nameID}")
            self.stdout.write(f"Name: {name.name}")
            self.stdout.write(f"Name Poster: {name.namePoster}")
            self.stdout.write(f"Birth Year: {name.birthYear}")
            self.stdout.write(f"Death Year: {name.deathYear}")
            self.stdout.write(f"Profession: {name.profession}")

            # Output the related participations
            participations = name.nameTitles.all()
            for participation in participations:
                self.stdout.write(f"Title ID: {participation.tconst}")
                self.stdout.write(f"Title: {participation.primaryTitle}")
                self.stdout.write(f"Category: {Participation.objects.get(name=name, movie=participation).category}")

        except Name.DoesNotExist:
            self.stdout.write(f"No name found with Name ID: {nameid}")
        except Exception as e:
            self.stdout.write(f"An error occurred: {e}")"""

    """def search_name(self, name):
        try:
            # Perform a case-insensitive search for names containing the input
            matching_names = Name.objects.filter(name__icontains=name)
            
            if matching_names.exists():
                self.stdout.write(f"Found {matching_names.count()} name(s) containing '{name}':")
                for name in matching_names:
                    self.stdout.write(f"Name ID: {name.nameID}, Name: {name.name}")
            else:
                self.stdout.write(f"No names found containing '{name}'.")

        except Exception as e:
            self.stdout.write(f"An error occurred: {e}")"""
#
    def import_episode(self, options):
        tsv_file = options['filename']
        with open(tsv_file, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                tconst = row['tconst']
                parentTconst = row['parentTconst'] if row['parentTconst'] != '\\N' else None
                seasonNumber = int(row['seasonNumber']) if row['seasonNumber'] != '\\N' else None
                episodeNumber = int(row['episodeNumber']) if row['episodeNumber'] != '\\N' else None

                try:
                    episode, created = Episode.objects.update_or_create(
                        tconst=tconst,
                        defaults={
                            'parentTconst': parentTconst,
                            'seasonNumber': seasonNumber,
                            'episodeNumber': episodeNumber,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created episode {episode}'))
                    else:
                        self.stdout.write(f'Updated episode {episode}')
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error creating/updating episode {tconst}: {e}'))
# ok 
    def import_rating(self, options):
        tsv_file = options['filename']
        with open(tsv_file, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                tconst = row['tconst']
                averageRating = float(row['averageRating']) if row['averageRating'] != '\\N' else None
                numVotes = int(row['numVotes']) if row['numVotes'] != '\\N' else None

                try:
                    rating, created = Ratings.objects.update_or_create(
                        tconst=tconst,
                        defaults={
                            'averageRating': averageRating,
                            'numVotes': numVotes,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created rating {rating}'))
                    else:
                        self.stdout.write(f'Updated rating {rating}')
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error creating/updating rating {tconst}: {e}'))
# ok
    def import_principals(self, options):
        tsv_file = options['filename']
        with open(tsv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                tconst = row['tconst']
                ordering = int(row['ordering'])
                nconst = row['nconst']
                category = row['category']
                job = None if row['job'] == '\\N' else row['job']
                characters = None if row['characters'] == '\\N' else row['characters']
                img_url_asset = None if 'img_url_asset' not in row or row['img_url_asset'] == '\\N' else row['img_url_asset']

                try:
                    principal, created = Principals.objects.update_or_create(
                        tconst=tconst,
                        ordering=ordering,
                        defaults={
                            'nconst': nconst,
                            'category': category,
                            'job': job,
                            'characters': characters,
                            'img_url_asset': img_url_asset,
                        }
                    )
                    action = "created" if created else "updated"
                    self.stdout.write(self.style.SUCCESS(f'Successfully {action} principals entry {principal}'))
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error {action} principals entry {tconst}: {e}'))

#
    def import_names(self, options):
        tsv_file = options['filename']
        with open(tsv_file, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                nconst = row['nconst']
                primaryName = row['primaryName']
                birthYear = None if row['birthYear'] == "\\N" else int(row['birthYear'])
                deathYear = None if row['deathYear'] == "\\N" else int(row['deathYear'])
                primaryProfession = None if row['primaryProfession'] == "\\N" else row['primaryProfession']
                knownForTitles = None if row['knownForTitles'] == "\\N" else row['knownForTitles']
                img_url_asset = None if 'img_url_asset' not in row or row['img_url_asset'] == "\\N" else row['img_url_asset']

                try:
                    person, created = Names.objects.update_or_create(
                        nconst=nconst,
                        defaults={
                            'primaryName': primaryName,
                            'birthYear': birthYear,
                            'deathYear': deathYear,
                            'primaryProfession': primaryProfession,
                            'knownForTitles': knownForTitles,
                            'img_url_asset': img_url_asset,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created person {person}'))
                    else:
                        self.stdout.write(f'Updated person {person}')
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error creating/updating person {nconst}: {e}'))

# ok
    def import_akas(self, options):
        tsv_file = options['filename']
        with open(tsv_file, 'r', encoding='utf-8') as file:  # Ensure correct encoding
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                titleId = row['titleId']
                ordering = int(row['ordering'])  # Ensure ordering is an integer
                title = row['title']
                region = None if row['region'] == '\\N' else row['region']
                language = None if row['language'] == '\\N' else row['language']
                types = None if row['types'] == '\\N' else row['types']
                attributes = None if row['attributes'] == '\\N' else row['attributes']
                isOriginalTitle = True if row.get('isOriginalTitle') == '1' else False  # Safely use .get for optional fields

                try:
                    akas_entry, created = Akas.objects.update_or_create(
                        titleId=titleId,
                        ordering=ordering,
                        defaults={
                            'title': title,
                            'region': region,
                            'language': language,
                            'types': types,
                            'attributes': attributes,
                            'isOriginalTitle': isOriginalTitle,
                        }
                    )
                    action = "created" if created else "updated"
                    self.stdout.write(self.style.SUCCESS(f'Successfully {action} Akas entry {akas_entry}'))
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error {action} Akas entry {titleId}: {e}'))
# ok 
    def import_titles(self, options):
        tsv_file = options['filename']
        with open(tsv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                tconst = row['tconst']
                titleType = row['titleType']
                primaryTitle = row['primaryTitle']
                originalTitle = row['originalTitle']
                isAdult = True if row['isAdult'] == '1' else False
                startYear = row['startYear'] if row['startYear'] != '\\N' else None
                endYear = row['endYear'] if row['endYear'] != '\\N' else None
                runtimeMinutes = int(row['runtimeMinutes']) if row['runtimeMinutes'] != '\\N' else None
                genres = row['genres'] if row['genres'] != '\\N' else None
                img_url_asset = row['img_url_asset'] if 'img_url_asset' in row and row['img_url_asset'] != '\\N' else None

                try:
                    movie, created = Movies.objects.update_or_create(
                        tconst=tconst,
                        defaults={
                            'titleType': titleType,
                            'primaryTitle': primaryTitle,
                            'originalTitle': originalTitle,
                            'isAdult': isAdult,
                            'startYear': startYear,
                            'endYear': endYear,
                            'runtimeMinutes': runtimeMinutes,
                            'genres': genres,
                            'img_url_asset': img_url_asset,
                        }
                    )
                    action = "created" if created else "updated"
                    self.stdout.write(self.style.SUCCESS(f'Successfully {action} movie entry {movie}'))
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Error {action} movie entry {tconst}: {e}'))

    def login_user(self, options):
        # Assuming you're receiving 'username' and 'password' as POST parameters
        username = options['username']
        password = options['password']
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # User is authenticated
            mydata = {
                'username': username,
                'password': password,
            }
            
            user = 'user.json'
            with open(user, 'w') as file:
                json.dump(mydata, file, indent=4)


            # Define the URL to which you want to make the POST request
            post_url = 'http://127.0.0.1:8000/application/x-www-form-urlencoded/'  # Change this to your actual endpoint URL
            
            # Make the POST request with JSON data
            headers = {'Content-Type': 'application/json'}  # Ensure the server expects JSON
            response = requests.post(post_url, json=mydata, headers=headers)
            
            # Check response status (optional)
            if response.status_code == 200:
                print("Data successfully posted.")
            else:
                print("Failed to post data. Status code:", response.status_code)
        else:
            print("Authentication failed.")