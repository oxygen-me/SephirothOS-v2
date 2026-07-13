"""Quotes displayed on the Home dashboard."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Quote:
    """Attributed quotation displayed by SephirothOS."""

    text: str
    author: str = "Sephiroth"


QUOTES: tuple[Quote, ...] = (
    Quote(
        "Is this the pain you felt before, Cloud? Let me remind you. This time you won't forget."
    ),
    Quote("On your knees! I want you to beg for forgiveness."),
    Quote("Good to see you, Cloud."),
    Quote("Tell me what you cherish most. Give me the pleasure of taking it away?"),
    Quote("I...will never be a memory."),
    Quote("Oh? Where did you find this strength?"),
    Quote("After a long sleep, time has come..."),
    Quote(
        "You are just a puppet...You have no heart...and cannot feel any "
        "pain... How can there be any meaning in the memory of such a "
        "being? What I have shown you is reality. What you remember, "
        "that is the illusion."
    ),
    Quote("Out of my way. I'm going to see my Mother."),
    Quote("What are you saying? Are you trying to tell me you have feelings too?"),
    Quote(
        "I have orders to take this planet back from you stupid people for the Cetra. What am I "
        "supposed to be sad about?"
    ),
    Quote("We meet at last...Mother."),
    Quote(
        "How does it feel? It's your first time in your hometown in a long time right? So how "
        "does it feel? I wouldn't know because I don't have a hometown."
    ),
    Quote("Ha, ha, ha. Think, Cloud? ...Cloud? Ha, ha, ha. Oh, excuse me. You never had a name..."),
    Quote(
        "Melding with the Planet... I will cease to exist as I am now... Only to be reborn as a "
        "'God' to rule over every soul."
    ),
    Quote(
        "Only death awaits you all, but do not fear. For it is through death that a new spirit "
        "energy is born. Soon, you will live again as a part of me."
    ),
    Quote("I've thought of a wonderful present for you...Shall I give you despair?"),
    Quote("Well, that's up to you, Cloud."),
    Quote("And on its soil, we'll create a shining future."),
    Quote("Stop pretending as if you're sad."),
    Quote(
        "Don't pretend you're sad. Why tremble with anger that's not even there? Face it, Cloud. "
        "You're just an empty puppet."
    ),
    Quote("How can I not, when you've beaten it into my head?"),
    Quote("Why couldn't I be the donor?"),
    Quote("Permission to return, granted."),
    Quote("Depending on what happens, I may abandon Shinra."),
    Quote(
        "Ever since I was a child, I knew I was not like the others... I knew mine was a "
        "special existence... But this, this was not what I meant! Am I—A human being?"
    ),
    Quote(
        "Genesis. Whether your words...are lies created to deceive me... or the truth that I "
        "have sought all my life... It makes no difference. You will rot."
    ),
    Quote("I have been chosen to rule this Planet."),
    Quote("Abominations spawned by Mako energy, that's what monsters are."),
    Quote(
        "You average SOLDIER members, are mako infused humans. You're enhanced, but you're "
        "still human, but then, what are those things, their mako energy levels "
        "are exponentially higher than yours."
    ),
    Quote("I am the Chosen One. I am the one chosen to rule this Planet."),
    Quote("Is that the best you can do?"),
    Quote("Hmph. Come and try."),
    Quote("Showing your back to the enemy? Overconfidence will destroy you..."),
    Quote("Angeal!"),
    Quote("You're annoying."),
)
