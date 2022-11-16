import random

def get_response(message: str) -> str:

    p_message = message.lower()

    if p_message == 'hello':
        return 'Hey there!'

    if p_message == "!standings west":
        result = """
**Western Conference Standings:**
1. Trail Blazers (10-4)
2. Nuggets (9-4)
3. Jazz (10-6)
4. Suns (8-5)
5. Mavericks (8-5)
6. Grizzlies (9-6)
7. Pelicans (8-6)
8. Kings (7-6)
9. Clippers (8-7)
10. Timberwolves (6-8)
11. Warriors (6-8)
12. Thunder (6-8)
13. Spurs (6-9)
14. Lakers (3-10)
15. Rockets (2-12)
        """
        return result

    if p_message == "!standings east":
        result = """
**Eastern Conference Standings:**
1. Celtics (11-3)
2. Bucks (10-3)
3. Hawks (9-5)
4. Cavaliers (8-5)
5. Wizards (8-6)
6. Raptors (8-7)
7. Knicks (7-7)
8. Pacers (6-6)
9. 76ers (7-7)
10. Heat (7-7)
11. Bulls (6-8)
12. Nets (6-9)
13. Magic (4-10)
14. Hornets (4-11)
15. Pistons (3-12)
        """
        return result

    if p_message == "!schedule":
        result = """
**Schedule for November 16, 2022:**
6:30 PM CST: Heat @ Raptors
6:30 PM CST: Celtics @ Hawks
7:00 PM CST: Cavaliers @ Bucks
7:00 PM CST: Bulls @ Pelicans
7:30 PM CST: Rockets @ Mavericks
9:00 PM CST: Warriors @ Suns
        """
        return result

    if p_message == '!trivia':
        x = (random.randint(1, 6))
        match x:
            case 1: 
                return """**Fun Fact #1:** 
Did you know? Shaquille O\'Neal has only made one 3 pointer in his NBA career!"""
            case 2:
                return """**Fun Fact #2:** 
Did you know? Kyle Lowry helped design the 2019 NBA final ring - the biggest and most expensive one to date!"""
            case 3:
                return """**Fun Fact  # 3:** 
Did you know? Giannis Antetokounmpo\'s family immigrated illegaly to Greece from Nigeria, where they lived in poverty until Giannis made it to the NBA and brought them with him."""
            case 4:
                return """**Fun Fact #4:**
Did you know? LeBron James has only missed the playoffs 4 times in his entire career!"""
            case 5:
                return """**Fun Fact  # 5:** 
Did you know? Michael Jordan\'s shoe deal with Nike for Jordans is one of the most successful partnerships of all time!"""
            case 6:
                return """**Fun Fact #6:** 
Did you know? Steph Curry\'s first name is actually Wardell. His middle name is Stephen!"""

    if p_message == '!help':
        return '`This is a help message that you can modify.`'

    return 'I don\'t understand.'