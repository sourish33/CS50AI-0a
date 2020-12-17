import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def get_movies(actor):
    return list(set(people[actor]['movies']))

def get_actors(mov):
    return list(set(movies[mov]['stars']))

def get_path(node, startNode, checked):
    
    path = []
    while(True):
        if node.parent == startNode.state:
#             print("Done")
            pathlet = (node.action, node.state)
#             print(pathlet)
            path.append(pathlet)
            break
        else:
            pathlet = (node.action, node.state)
#             print(pathlet)
            path.append(pathlet)
            node = checked.get_node_with_state(node.parent)

    path.reverse()
    return path
            

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target, searchtype=1):
    if (source == target):
        return []
    if not source in people.keys() or not target in people.keys():
        print("source or target not in database")
        return []
    if searchtype == 1:
        Frontier = QueueFrontier()
    else:
        Frontier = StackFrontier()
    checked = StackFrontier()
    startNode = Node(source,None,None)
    Frontier.add(startNode)
    foundNode = None
    path = []

    n=0
    while(True):
        removedNode = Frontier.remove()
        checked.add(removedNode)
        removedState = removedNode.state
        if (n%500==0):
            print("Iteration {}: frontier size: {} checked size {}".format(n, Frontier.length(), checked.length()))

        theirMovies = get_movies(removedState)
        newNodeList = []
        checkedList = checked.state_list()
        currentList = Frontier.state_list()
        # current_actors = Frontier.state_list()

        for mov in theirMovies:
            actors = get_actors(mov)
            actors = [x for x in actors if not x in currentList and not x in checkedList]
            if target in actors:
                print("Success!!! after {} iterations".format(n))
                foundNode = Node(target,removedState,mov)
                path = get_path(foundNode,startNode,checked)
                return path
            else:
                NodeList = [Node(x, removedState, mov) for x in actors]
                newNodeList+=NodeList
        Frontier.add(newNodeList)
        n+=1
        if Frontier.length()<1:
            print("search failed after {} iterations".format(n))
            break

    return path



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
