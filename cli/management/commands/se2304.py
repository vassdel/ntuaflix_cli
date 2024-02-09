from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError
import json
from cli.models import Movie
from cli.models import Name
from cli.models import Participation

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
        addcrew_parser = subparsers.add_parser('addcrew')
        addcrew_parser.add_argument('--tconst', required=True)
        addcrew_parser.add_argument('--directors', required=True)
        addcrew_parser.add_argument('--writers', required=True)

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


    def add_user(self, username, password):
        try:
            # Create a new user instance and save it to the database
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Output message
            self.stdout.write(f"User {username} added successfully.")

        except IntegrityError:
            self.stdout.write(f"User {username} already exists.")
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
            movie = Movie.objects.create(
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
        movies = Movie.objects.all()
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
        matching_movies = Movie.objects.filter(originalTitle__icontains=titlePart)
        if matching_movies.exists():
            self.stdout.write(f"Found {matching_movies.count()} movie(s) matching '{titlePart}':")
            for movie in matching_movies:
                self.stdout.write(f"ID: {movie.id}, Title: {movie.originalTitle}")
        else:
            self.stdout.write(f"No movies found matching '{titlePart}'.")

    def search_by_genre(self, genre, yrFrom=None, yrTo=None, min_rating=None):
        # Start with a query for movies matching the genre
        matching_movies = Movie.objects.filter(genres__icontains=genre)

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

    def add_name(self, options):
        try:
            # Create the name entry
            name = Name.objects.create(
                nameID=options['nameID'],
                name=options['name'],
                namePoster=options.get('namePoster'),
                birthYear=options.get('birthYear'),
                deathYear=options.get('deathYear'),
                profession=options.get('profession'),
            )

            # Create the participation entry if titleID and category are provided
            if options.get('titleID') and options.get('category'):
                movie = Movie.objects.get(tconst=options['titleID'])
                Participation.objects.create(
                    name=name,
                    movie=movie,
                    category=options['category']
                )

            # Output message
            self.stdout.write(f"Producer {name.name} added successfully.")

        except Exception as e:
            self.stdout.write(f"An error occurred: {e}")

    def show_name(self, nameid):
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
            self.stdout.write(f"An error occurred: {e}")

    def search_name(self, name):
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
            self.stdout.write(f"An error occurred: {e}")
