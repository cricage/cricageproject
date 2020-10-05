import pyrebase
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponseRedirect

config = {
    'apiKey': "AIzaSyCXOo5sLbHbTbQXZ0q7nk-g8Hrp9SCm8-0",
    'authDomain': "cricage-50006.firebaseapp.com",
    'databaseURL': "https://cricage-50006.firebaseio.com",
    'projectId': "cricage-50006",
    'storageBucket': "cricage-50006.appspot.com",
    'messagingSenderId': "1097691081450",
    'appId': "1:1097691081450:web:fe1cb6c93ff05f73600593",
    'measurementId': "G-VL8VYEYHXN"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def singIn(request):
    return render(request, "myScore/signIn.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        print("Signing in")
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        print("Failed")
        message = "invalid cerediantials"
        return render(request, "myScore/signIn.html", {"msg": message})
    print(user)
    return render(request, "myScore/postsign.html", {"e": email})


def logout(request):
    auth.logout(request)
    return render(request, "myScore/signIn.html")


def create_team(request):
    ddict = {}
    try:
        teams = list(database.child("Teams").get().val())
    except TypeError:
        teams = []
    ddict["Teams"] = teams
    if request.method == "POST":
        name = request.POST.get('teamname')
        location = request.POST.get('location')
        data = {"Location": location}

        if name not in teams:
            database.child("Teams").child(name).set(data)
            ddict["msg"] = "Data Saved"
        else:
            ddict["msg"] = "Team Already Exist"
    return render(request, "myScore/create_team.html", ddict)


def add_player(request):
    ddict = {}



    if request.method == "POST":
        data = {}
        data["name"] = request.POST.get('name')
        phone = request.POST.get('phone')
        data["age"] = request.POST.get('age')
        try:
            players = list(dict(database.child("Players").get().val()).keys())
        except TypeError:
            players = []
        if phone not in players:
            database.child("Players").child(phone).set(data)
            ddict["new"] = phone
        else:
            ddict["msg"] = "Player already exists"


    try:
        players = dict(database.child("Players").get().val())
    except TypeError:
        players = {}
    ddict["players"] = list(players)

    return render(request, "myScore/addplayer.html", ddict)


def matching(request):
    ddict = {}
    try:
        teams = dict(database.child("Teams").get().val())
    except TypeError:
        teams = {}
    try:
        players = dict(database.child("Players").get().val())
    except TypeError:
        players = {}

    ddict["teams"] = list(teams.keys())
    ddict["players"] = list(players.keys())

    if request.method == "GET":
        request.session.clear()

    if request.method == "POST":
        team1 = request.POST.get("team1")
        team2 = request.POST.get("team2")
        player1 = request.POST.get("player1")
        player2 = request.POST.get("player2")
        timeval = request.POST.get("timeval")

        if team1:
            ddict["team1selected"] = request.POST.get("team1")
        if team2:
            ddict["team2selected"] = request.POST.get("team2")

        if player1:
            if not request.session.get("playerteam1"):
                request.session["playerteam1"] = []
            plist1 = request.session['playerteam1']
            plist1.append(player1)
            request.session["playerteam1"] = plist1

        if player2:
            if not request.session.get("playerteam2"):
                request.session["playerteam2"] = []
            plist2 = request.session['playerteam2']
            plist2.append(player2)
            request.session["playerteam2"] = plist2

        if timeval:
            request.session["timestamp"] = timeval
            data = {"Team1": team1, "Team2": team2, "PlayersTeam1": request.session["playerteam1"],
                    "PlayersTeam2": request.session["playerteam2"]}

            tosswin = request.POST["tossinput"]
            tosschoice = request.POST["toss_choice"]

            if tosswin == "Team 1":
                if tosschoice == "Bowling":
                    data["batFirstTeam"] = team2
                    data["bowlFirstTeam"] = team1

                else:
                    data["batFirstTeam"] = team1
                    data["bowlFirstTeam"] = team2
            else:
                if tosschoice == "Bowling":
                    data["batFirstTeam"] = team1
                    data["bowlFirstTeam"] = team2

                else:
                    data["batFirstTeam"] = team2
                    data["bowlFirstTeam"] = team1

            database.child("Match").child(timeval).set({"Status": "Not_Started"})
            database.child("Match").child(timeval).child("Team_Details").set(data)
            request.session["OverCount"] = 1
            request.session["BallCount"] = 0
            return redirect("score")

        a = set(request.session.get("playerteam1", "x")).union(set(request.session.get("playerteam2", "x")))
        ddict["players"] = list(set(list(players.keys())).difference(a))
        print(ddict["players"])

    return render(request, "myScore/match.html", ddict)


def score(request):
    ddict = {}
    print("%%%%%%%%%%%%%%%%%%%%")
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    print("%%%%%%%%%%%%%%%%%%%%")

    teamdata = dict(database.child("Match").child(request.session["timestamp"]).child("Team_Details").get().val())
    ddict["BatTeam"] = teamdata["batFirstTeam"]
    ddict["BowlTeam"] = teamdata["bowlFirstTeam"]
    ddict["BatTeamPlayers"] = teamdata["PlayersTeam1"] if teamdata["batFirstTeam"] == teamdata["Team1"] else teamdata[
        "PlayersTeam2"]
    ddict["BowlTeamPlayers"] = teamdata["PlayersTeam1"] if teamdata["bowlFirstTeam"] == teamdata["Team1"] else teamdata[
        "PlayersTeam2"]


    print(ddict)

    if request.method == "POST":
        print("$$$$$$$%%%%$$%%")
        for k in request.POST.items():
            print(k)
            try:
                print(k, request.POST[k])
            except:
                pass
        print("$$$$$$$%%%%$$%%")

        if request.POST.get("batsman1"):
            request.session["player1"] = request.POST.get("batsman1")
        if request.POST.get("batsman2"):
            request.session["player2"] = request.POST.get("batsman2")
        if request.POST.get("bowler"):
            request.session["bowler"] = request.POST.get("bowler")

            print("@@@@@@#######")
            for key, value in request.session.items():
                print('{} => {}'.format(key, value))
            print("@@@@@@#######")

        if request.session["BallCount"] == 6:
            
            request.session["OverCount"] += 1
            request.session["BallCount"] = 0

        if request.POST.get("one"):
            request.session["BallCount"] += 1
            bdata = {"batsman1": request.session.get("batsman1"), "batsman2": request.session.get("batsman2"), "bowler": request.session.get("bowler"), "Runs": 1}
            database.child("Match").child(request.session["timestamp"]).child("Score").child("Over").child(
                request.session.get("OverCount")).child("Balls").child(request.session.get("BallCount")).set(bdata)

        if request.POST.get("two"):
            request.session["BallCount"] += 1
            bdata = {"batsman1": request.session.get("batsman1"), "batsman2": request.session.get("batsman2"), "bowler": request.session.get("bowler"), "Runs": 2}
            database.child("Match").child(request.session["timestamp"]).child("Score").child("Over").child(
                request.session.get("OverCount")).child("Balls").child(request.session.get("BallCount")).set(bdata)
        if request.POST.get("three"):
            request.session["BallCount"] += 1
            bdata = {"batsman1": request.session.get("batsman1"), "batsman2": request.session.get("batsman2"), "bowler": request.session.get("bowler"), "Runs": 3}
            database.child("Match").child(request.session["timestamp"]).child("Score").child("Over").child(
                request.session.get("OverCount")).child("Balls").child(request.session.get("BallCount")).set(bdata)
        if request.POST.get("four"):
            request.session["BallCount"] += 1
            bdata = {"batsman1": request.session.get("batsman1"), "batsman2": request.session.get("batsman2"), "bowler": request.session.get("bowler"), "Runs": 4}
            database.child("Match").child(request.session["timestamp"]).child("Score").child("Over").child(
                request.session.get("OverCount")).child("Balls").child(request.session.get("BallCount")).set(bdata)
        if request.POST.get("six"):
            request.session["BallCount"] += 1
            bdata = {"batsman1": request.session.get("batsman1"), "batsman2": request.session.get("batsman2"), "bowler": request.session.get("bowler"), "Runs": 6}
            database.child("Match").child(request.session["timestamp"]).child("Score").child("Over").child(
                request.session.get("OverCount")).child("Balls").child(request.session.get("BallCount")).set(bdata)
        if request.POST.get("wide"):
            bdata = {"batsman1": request.session.get("batsman1"), "batsman2": request.session.get("batsman2"), "bowler": request.session.get("bowler"), "Runs": 1}
            database.child("Match").child(request.session["timestamp"]).child("Score").child("Over").child(
                request.session.get("OverCount")).child("Balls").child("wide").set(bdata)
        if request.POST.get("nbs"):
            bdata = {"batsman1": request.session.get("batsman1"), "batsman2": request.session.get("batsman2"), "bowler": request.session.get("bowler")}
            if request.POST.get("nbs") == "noball":
                bdata["Runs"]: 1
            if request.POST.get("nbs") == "noball_1":
                bdata["Runs"]: 2
            if request.POST.get("nbs") == "noball_2":
                bdata["Runs"]: 3
            if request.POST.get("nbs") == "noball_3":
                bdata["Runs"]: 4
            if request.POST.get("nbs") == "noball_4":
                bdata["Runs"]: 5
            if request.POST.get("nbs") == "noball_6":
                bdata["Runs"]: 7
            if request.POST.get("nbs") == "noball_RO":
                bdata["Runs"]: 1

            database.child("Match").child(request.session["timestamp"]).child("Score").child("Over").child(
                request.session.get("OverCount")).child("Balls").child("Noball").set(bdata)

        if request.POST.get("wicket"):
            request.session["BallCount"] += 1
            bdata = {"batsman1": request.session.get("batsman1"), "batsman2": request.session.get("batsman2"), "bowler": request.session.get("bowler"),"wicket":request.POST.get("wicket")}
            database.child("Match").child(request.session["timestamp"]).child("Score").child("Over").child(
                request.session.get("OverCount")).child("Balls").child("Wicket").set(bdata)
            if request.POST.get("wicket") == "Bowled" or request.POST.get("wicket") == "Caught" or request.POST.get("wicket") == "LBW" or request.POST.get("wicket") == "Stumped" or request.POST.get("wicket") == "Hittheballtwice" or request.POST.get("wicket") == "Hitwicket":
                del request.session["player1"]
            else:
                del request.session["player2"]
        
    print(ddict)
    return render(request, "myScore/score.html", ddict)
