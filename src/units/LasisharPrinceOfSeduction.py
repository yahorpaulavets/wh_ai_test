from src.models.BattleModel import BattleModel, RangeWeapon, WeaponKeywords, MeleeWeapon, Abilities, CoreAbilities, \
    Factions, PersonalAbilities


class LasisharPrinceOfSeduction(BattleModel):
    def __init__(self):
        super().__init__()

        self.name = "Ласишар Принц Искушения"
        self.M = 9
        self.T = 8
        self.SV = 3
        self.ISV = 4
        self.W = 18
        self.LD = 8
        self.OC = 6

        rw1 = RangeWeapon()
        rw1.name = "Эмонация Боли"
        rw1.R = 20
        rw1.AN = 6
        rw1.BS = 2
        rw1.S = 16
        rw1.AP = -4
        rw1.D = "D6 + 3"
        rw1.keywords = [WeaponKeywords.LETHAL_HITS, WeaponKeywords.PSYCHIC]

        rw2 = RangeWeapon()
        rw2.name = "Эмонация Боли (Сфокусированный Заряд)"
        rw2.R = 70
        rw2.AN = 1
        rw2.BS = 2
        rw2.S = 20
        rw2.AP = -6
        rw2.D = "6 + D3"
        rw2.keywords = [WeaponKeywords.PSYCHIC, WeaponKeywords.PRECISE]

        rw3 = RangeWeapon()
        rw3.name = "Темный скипетер - варп разрыв"
        rw3.R = 35
        rw3.AN = 12
        rw3.BS = 1
        rw3.S = 10
        rw3.AP = -3
        rw3.D = "D6"
        rw3.keywords = [WeaponKeywords.PSYCHIC, WeaponKeywords.TORENT, WeaponKeywords.IGNORE_COVER]

        self.range_weapon = [rw1, rw2, rw3]

        mw1 = MeleeWeapon()
        mw1.name = "Спаренные блаженные клинки"
        mw1.AN = 6
        mw1.WS = 2
        mw1.S = 6
        mw1.AP = -4
        mw1.D = 3
        mw1.keywords = [WeaponKeywords.POISON, WeaponKeywords.DISSECTING, WeaponKeywords.TWIN]

        mw2 = MeleeWeapon()
        mw2.name = "Отравленные когти"
        mw2.AN = 18
        mw2.WS = 2
        mw2.S = 6
        mw2.AP = -3
        mw2.D = 2
        mw2.keywords = [WeaponKeywords.POISON_D3]

        mw3 = MeleeWeapon()
        mw3.name = "Темный скипетер - касание варпа"
        mw3.AN = 4
        mw3.WS = 2
        mw3.S = 20
        mw3.AP = -6
        mw3.D = 6
        mw3.keywords = [WeaponKeywords.PSYCHIC]

        self.melee_weapon = [mw1, mw2, mw3]

        a = Abilities()
        a.core = [CoreAbilities.FIGHT_FIRST]
        a.faction = [Factions.DAEMONS_OF_SLAANESH]
        a.personal = [PersonalAbilities.PRINCE_OF_SEDUCTION, PersonalAbilities.VAMPIRE, PersonalAbilities.SEDUCTION_OF_ENEMY]
        self.abilities = a
