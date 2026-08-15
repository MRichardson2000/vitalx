import random


QUOTES: list[str] = [
    # Darby Hudson Poem quotes
    "We're all weird. Everyone's pretending. No one knows what they're doing. Do whatever you want. Have you tried that yet? It's fucking amazing!",
    "Death wants you alive and life wants you dead",
    "It's worth being born into this world just to quit a shitty job",
    "Sure, strive to be better than you were yesterday but remember to fuck up massively from time to time to reset the difficulty level",
    "Swearing removes the pain of life for just a second. It's small, it's cheap... but relief is fuckin' relief!",
    "You're going to be okay because you're fucked no matter what!",
    "Buying the most expensive house or boat will not prevent you from being trapped in your head at night",
    "Tomorrow is for people with plans, today is for people with art!",
    "Don't forget to smuggle your 3 A.M. self into all of your 3 P.M's",
    "Starting anything takes guts. Knowing when to finish takes style",
    "A job interview is where you have to prove you're worthy of staying alive by pretending that your dead",
    "Employment is where you're paid to turn strangers into friends, then back into strangers, until you become a stranger to yourself...",
    "Don't forget to mark all management emails as spam",
    "Attention to detail isn't a resume thing, it's a noticing-the-clouds thing",
    "Never check your reflection at work, because it's like waking mid surgery. Your spirit will go into quiet shock",
    "Linkedin success story: I failed and failed. Then, with my last two dollars, I hailed a cab, traveled ten yards down the street, got out. Then the sun came out , a leaf blew from a tree, a bird sang and I was rich",
    "Make sure you try and run out of time and money on the same day, Like trying to land a jumbo jet straight into a coffin",
    "Stay in a job for only two pairs of worn-out shoes. Longer, and you're walking in circles.",
    "'Above and beyond' is something to write on your gravestone not your resume",
    "I miss when the years were marked in colors and scents and animals and insects not numbers",
    "The pile of unread books by your bed is a small staircase to your unslept dreams",
    "I like stories with weather in them. When a book mentions rain I need to put it down and dream",
    "I enter the room, the room enters me. I vanish",
    "My happiness is directly proportionate to the distance I am from my bed",
    "Dear diary, today I had a lovely afternoon nap in the cemetary. Just practicing",
    "My Shadow is a black sack full of last nights dreams. Emptied of stars",
    "Time is loaded with endless night... Sleep is a velvet gunshot to the head - A star splattered sky",
    "Time is always changing the locks and throwing away the keys",
    "We are born out of dream before being blown back across the sky, a skeleton of stars",
    "Sometimes a fuck up isn't really a fuck up. It's the angel on the shoulder of the devil on your shoulder",
    "You are made of stardust! And poo particles... Don't get ahead of yourself",
    "My business is none of my business, sometimes I don't give a shit what i've been up to",
    "My favourite people aren't courageous; They just weren't listening to all the crap and forgot to be scared",
    "You are not a bad listender, ninety nine percent of people are fucking boring",
    "There are days when you just have to cockroach the shit out of life - you got this king!",
    "Leaving is the loveliest form of arriving",
    "Everything you do or say will be used against you by your brain so stop giving a fuck",
    "If someone's building you a pedestal, they're also digging you a grave",
    "The only way to become a sleepwalker is to ditch the narrative, lose the plot, and remember: Mistakes and dreams are holy",
    "People reverse park their cars in the supermarket parking lot to gain control over what little they can",
    "Things suck, then things don't suck, then things suck again. This loop is so infinite and dizzying, i'm never sure which is payment for the other",
    "There was once an old man who worked on his suicide note his entire life before dying of old age",
    "Survive the world's lies long enough and eventually the only thing that makes sense is bullshit. But the sacred bullshit - like love, birds, sky, trees, nights, moonlight",
    "Current culture: Fake it until you're completely fake",
    "'Screw it' gets me out of bed and saying it quickly a second time gets me straight back into bed",
]


def get_random_quote() -> str:
    return random.choice(QUOTES)


def main() -> None:
    print(get_random_quote())


if __name__ == "__main__":
    main()
