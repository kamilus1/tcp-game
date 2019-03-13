from random import randint


class Skills(object):
    @classmethod
    def basic(cls, dmg, to=None, who=None):
        if to != None:
            who.sendto(str(dmg).encode("utf-8"), to)
        else:
            return dmg
    @classmethod
    def critic(cls, dmg, chance,mana, to=None, who=None):
        dmg -= 1
        add = randint(int(chance/2), chance)
        dmg += add
        mana -= 1
        if to != None:
            who.sendto(str(dmg).encode("utf-8"), to)
        else:
            return dmg, mana

        return mana
    @classmethod
    def heal(cls, hp, max, mana, who=None, to=None ):
        max -= hp
        max /= 2
        max = round(max)
        hp += max
        mana -= 2
        if who != None:
            who.sendto("0".encode("utf-8"), to)
        return int(hp), mana
    @classmethod
    def harnas_vomit(cls, hp, dmg, who=None, to=None):
        dmg += dmg*2/hp
        hp -= 1
        if who != None:
            who.sendto(str(dmg).encode("utf-8"), to)
        else:
            return dmg, hp
        return hp
    @classmethod
    def tatra_shot(cls, dmg, mana, who=None, to=None):
        if mana > 5:
            mana -= 5
            dmg *= 2
        if who != None:
            who.sendto(str(dmg).encode("utf-8"), to)
        return dmg, mana

