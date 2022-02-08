from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QButtonGroup, QApplication, QTableWidgetItem
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("pokemonDB.ui", self)
        self.initComboBox()
        self.initRadBtns()
        self.connectToDb()
        self.loadInitialData()
        self.handleButtons()
        
    def connectToDb(self):
        # Connect to db
        self.connection = sqlite3.connect('pokemon.db')
        self.cur = self.connection.cursor()

    def loadInitialData(self):
        self.handlePokemon()

    def handleButtons(self):
        self.pokemon.clicked.connect(self.handlePokemon)
        self.generation.clicked.connect(self.handleGeneration)
        self.ability.clicked.connect(self.handleAbility)
        self.forms.clicked.connect(self.handleForms)
        self.types.clicked.connect(self.handleTypes)
        self.typeDamage.clicked.connect(self.handleTypeDamage)
        self.moves.clicked.connect(self.handleMoves)
        self.version.clicked.connect(self.handleVersions)
        self.versionGroup.clicked.connect(self.handleVersionGroups)
        self.items.clicked.connect(self.handleItems)
        self.regularEvo.clicked.connect(self.handleRegularEvo)
        self.uniqueEvo.clicked.connect(self.handleUniqueEvo)
        self.encounterSlots.clicked.connect(self.handleEncounterSlot)
        self.encounterMethod.clicked.connect(self.handleEnounterMethods)
        self.regions.clicked.connect(self.handleRegions)
        self.locations.clicked.connect(self.handleLocations)
        self.areas.clicked.connect(self.handleAreas)
        self.eggGroups.clicked.connect(self.handleEggGroups)
        self.learnMethod.clicked.connect(self.handleLearnMethods)
        self.pkmnMoveVrsnLrn.clicked.connect(self.handlePkmnMoveVrsnLrn)
        self.pokemonForms.clicked.connect(self.handlePokemonForms)
        self.pokemonTypes.clicked.connect(self.handlePokemonTypes)
        self.formTypes.clicked.connect(self.handleFormTypes)
        self.machines.clicked.connect(self.handleMachines)
        self.pkmnAreaVrsnEnc.clicked.connect(self.handlePkmnAreaVrsnEnc)
        self.pokemonAbilities.clicked.connect(self.handlePokemonAbilities)
        self.pokemonEggGroups.clicked.connect(self.handlePokemonEggGroups)
        
        # Queries
        self.weightButton.clicked.connect(self.handleWeight)
        self.statsButton.clicked.connect(self.handleStats)
        self.numMovesPerType.clicked.connect(self.handleNumMoves)
        self.startingLetterBtn.clicked.connect(self.handleNames)
        self.legendEvo.clicked.connect(self.handleLegendEvo)
        self.greaterThanTwo.clicked.connect(self.handleMoreThanTwoMoves)
        self.pokemonTypeDist.clicked.connect(self.handleDist)
        self.palindromeNames.clicked.connect(self.handlePalindrome)
        self.noEvoBtn.clicked.connect(self.handleNoEvoLine)
        self.avgHeightEggGroup.clicked.connect(self.handleAvgHeight)


    def handleWeight(self):
        heavy = "SELECT pokemonName, weight FROM Pokemon ORDER by weight DESC limit 5"
        light = "SELECT pokemonName, weight FROM Pokemon ORDER by weight limit 5"

        labels = ["pokemonName", "weight (kg)"]
        if self.heavyRad.isChecked():
            self.handleTable(heavy, labels, "Heaviest Pokemon")
        else:
            self.handleTable(light, labels, "Lightest Pokemon")

    
    def handleStats(self):
        highest = "SELECT pokemonName, hp + attack + defense + spAtk + spDef + speed as totalBaseStat FROM Pokemon ORDER by totalBasestat DESC limit 5"
        lowest = "SELECT pokemonName, hp + attack + defense + spAtk + spDef + speed as totalBaseStat FROM Pokemon ORDER by totalBasestat limit 5"
        labels = ["pokemonName", "stats"]

        if self.highRad.isChecked():
            self.handleTable(highest, labels, "Pokemon with highest stats")
        else:
            self.handleTable(lowest, labels, "Pokemon with lowest stats")
    
    def handleNumMoves(self):
        most = "SELECT Moves.typeID, typeName, count(*) as numberOfMoves FROM Moves LEFT JOIN Types ON Types.typeID = Moves.typeID GROUP BY Moves.typeID HAVING count(Moves.typeID) ORDER BY numberOfMoves DESC"
        least = "SELECT Moves.typeID, typeName, count(*) as numberOfMoves FROM Moves LEFT JOIN Types ON Types.typeID = Moves.typeID GROUP BY Moves.typeID HAVING count(Moves.typeID) ORDER BY numberOfMoves"
        labels = ["typeID", "typeName", "numberOfMoves"]

        if self.mostRad.isChecked():
            self.handleTable(most, labels, "Type with most number of moves")
        else:
            self.handleTable(least, labels, "Type with least number of moves")

    def handleNames(self):
        beg = """SELECT pokemonName, vGroupID, count(*) as numOfMoves
                FROM PkmnVrsnMoveLrn
                Left JOIN Pokemon ON PkmnVrsnMoveLrn.pokemonID = Pokemon.pokemonID
                WHERE pokemonName in (
                SELECT pokemonName
                    FROM Pokemon
                    WHERE pokemonName LIKE '"""
        letter = self.comboBox.currentText()
        end = """%'
                )
                GROUP BY pokemonName, vGroupID
                HAVING count(moveID)
                ORDER BY PkmnVrsnMoveLrn.pokemonID
                """
        labels = ["pokemonName", "vGroupID", "numOfMoves"]
        self.handleTable(beg+letter+end, labels, "Number of moves " + letter + " Pokemon can learn in a version group")

    def handleLegendEvo(self):
        query = """SELECT pokemonID, pokemonName
                    FROM Pokemon
                    WHERE Pokemon.pokemonID in(
                        SELECT pokemonID1
                        FROM RegularEvolution
                        WHERE Pokemon.pokemonID = RegularEvolution.pokemonID1
                    ) AND isLegendary = 'TRUE'
                    """
        labels = ["pokemonID", "pokemonName"]
        self.handleTable(query, labels, "Legendary Pokemon that can evolve")

    def handleMoreThanTwoMoves(self):
        query = """SELECT pokemonID, pokemonName, count(*)
                    FROM PkmnAbilities
                    NATURAL JOIN Pokemon
                    GROUP BY pokemonID
                    HAVING count(distinct abilityID) > 2;
                    """
        labels = ["pokemonID", "pokemonName", "numberOfPotentialAbilities"]
        self.handleTable(query, labels, "Pokemon with more than 2 potential abilities")

    def handleDist(self):
        query = """SELECT regionID, regionName, typeName, printf("%.2f", 100.0 * count(*) / (
                        SELECT count(*)
                        FROM Regions
                        Natural JOIN Pokemon
                        Natural JOIN PokemonType
                        LEFT JOIN Types on PokemonType.typeID = Types.typeID
                        GROUP BY regionID
                        HAVING count(PokemonType.typeID)
                        Order by regionID
                    )) As percentage
                    FROM Regions
                    Natural JOIN Pokemon
                    Natural JOIN PokemonType
                    LEFT JOIN Types on PokemonType.typeID = Types.typeID
                    GROUP BY regionID, PokemonType.typeID
                    Order by regionID
                    """
        labels = ["regionID", "regionName", "typeName", "Percent"]
        self.handleTable(query, labels, "Type distribution per region")



    def handlePokemon(self):
        query = "SELECT * FROM Pokemon"
        labels = ["pokemonID","pokemonName","baseExp","hp","attack",
                  "defense","spAtk","spDef","speed","height",
                  "weight","genderRate","captureRate","growthRate","baseHappiness",
                  "formSwitchable","shape","genusName","color","hasGenderDiff",
                  "hatchCounter","isMythical","isLegendary","isBaby","genID"]
        self.handleTable(query, labels, "Pokemon")

    def handlePalindrome(self):
        # No reverse in sqlite 
        query = """SELECT pokemonId, pokemonName
                    FROM Pokemon
                    WHERE pokemonName in (
                        WITH reverse(i, c) AS 
                        (
                            values(-1, '')
                            UNION ALL SELECT i-1, substr(pokemonName, i, 1) AS r FROM reverse
                            WHERE r!=''
                        ) 
                        SELECT group_concat(c, '') AS reversed FROM reverse
                    )
                    """
        labels = ["pokemonID", "pokemonName"]
        self.handleTable(query, labels, "Palindrome Names")

    def handleNoEvoLine(self):
        query = """SELECT pokemonID, pokemonName
                    FROM Pokemon
                    WHERE pokemonID not in (
                        SELECT RegularEvolution.pokemonID1
                        FROM RegularEvolution
                        LEFT JOIN UniqueEvolution on RegularEvolution.pokemonID1 = UniqueEvolution.pokemonID1
                    )
                    AND
                    pokemonID not in (
                        SELECT RegularEvolution.pokemonID2
                        FROM RegularEvolution
                        LEFT JOIN UniqueEvolution on RegularEvolution.pokemonID1 = UniqueEvolution.pokemonID1
                    )
                    AND isLegendary = 'FALSE' AND isMythical = 'FALSE'
                    """
        labels = ["pokemonID", "pokemonName"]
        self.handleTable(query, labels, "Pokemon that are in an evolution line")

    def handleAvgHeight(self):
        query = """SELECT eggGroupID, groupName, printf("%.2f", avg(height)/10) as "avgHeight (m)"
                    FROM PkmnEggGroup
                    NATURAL JOIN Pokemon
                    NATURAL JOIN EggGroup
                    GROUP by eggGroupID"""
        labels = ["eggGroupID", "groupName", "avgHeight (m)"]
        self.handleTable(query, labels, "Average height of egg groups")

    def handleGeneration(self):
        query = "SELECT * FROM Generation"
        labels = ["genID","genName","regiondID"]
        self.handleTable(query, labels, "Generation")

    def handleAbility(self):
        query = "SELECT * FROM Ability"
        labels = ["abilityID","abilityName","description","genID"]
        self.handleTable(query, labels, "Ability")

    def handleForms(self):
        query = "SELECT * FROM Forms"
        labels = ["formName","formOrder","isDefault","isMega","isBattleOnly",
                  "fBaseExp","fHp","fAttack","fDef","fSpAtk",
                  "fSpDef","fSpeed","fHeight","fWeight"]
        self.handleTable(query, labels, "Forms")

    def handleTypes(self):
        query = "SELECT * FROM Types"
        labels = ["typeID", "typeName", "genID"]
        self.handleTable(query, labels, "Types")

    def handleTypeDamage(self):
        query = "SELECT * FROM TypeDamageRelation"
        labels = ["typeID", "targetTypeID", "damageAmount"]
        self.handleTable(query, labels, "Type Damage Relations")

    def handleMoves(self):
        query = "SELECT * FROM Moves"
        labels = ["moveID","moveName","typeID","category","power",
                  "accuracy","pp","effect","effectChance","priority",
                  "genID"]
        self.handleTable(query, labels, "Moves")

    def handleVersions(self):
        query = "SELECT * FROM Version"
        labels = ["versionID", "vGroupID", "versionName"]
        self.handleTable(query, labels, "Versions")

    def handleVersionGroups(self):
        query = "SELECT * FROM VersionGroup"
        labels = ["vGroupID", "groupName", "genID"]
        self.handleTable(query, labels, "Version Groups")
    
    def handleItems(self):
        query = "SELECT * FROM Items"
        labels = ["itemID","itemName","category","description","cost",
                  "flingPower","flingEffect"]
        self.handleTable(query, labels, "Items")

    def handleRegularEvo(self):
        query = "SELECT * FROM RegularEvolution"
        labels = ["evolutionID","pokemonID1","pokemonID2","minLevel","minHappiness",
                  "minAffection","gender","physicalStats","knownMoveType","timeOfDay",
                  "itemUsed","itemHeld","locationID","trigger"]
        self.handleTable(query, labels, "Regular Evolution")

    def handleUniqueEvo(self):
        query = "SELECT * FROM UniqueEvolution"
        labels = ["pokemonID1","pokemonTradeID","pokemonPresentID","minBeauty","needRain",
                  "turnUpsideDown","typePresentInParty","knownMoveID"]
        self.handleTable(query, labels, "Unique Evolution")

    def handleEncounterSlot(self):
        query = "SELECT * FROM EncounterSlot"
        labels = ["eSlotID", "eMethodID", "vGroupID", "slot", "rarity"]
        self.handleTable(query, labels, "Encounter Slots")

    def handleEnounterMethods(self):
        query = "SELECT * FROM EncounterMethod"
        labels = ["eMethodID", "eMethodName"]
        self.handleTable(query, labels, "Encounter Methods")

    def handleRegions(self):
        query = "SELECT * FROM Regions"
        labels = ["regionID", "regionName", "genID"]
        self.handleTable(query, labels, "Regions")

    def handleLocations(self):
        query = "SELECT * FROM Locations"
        labels = ["locationID", "locationName", "regionID"]
        self.handleTable(query, labels, "Locations")

    def handleAreas(self):
        query = "SELECT * FROM Areas"
        labels = ["areaID", "areaName", "locationID"]
        self.handleTable(query, labels, "Areas")

    def handleEggGroups(self):
        query = "SELECT * FROM EggGroup"
        labels = ["eggGroupID", "groupName"]
        self.handleTable(query, labels, "Egg Groups")

    def handleLearnMethods(self):
        query = "SELECT * FROM LearnMethod"
        labels = ["methodID", "methodName"]
        self.handleTable(query, labels, "Learn Methods")

    def handlePkmnMoveVrsnLrn(self):
        # TOO SLOW
        query = "SELECT * FROM PkmnVrsnMoveLrn"
        labels = ["pokemonID", "vGroupID", "moveID", "methodID"]
        # self.handleTable(query, labels, "Pokemon-Move-Version-Learn")

        # Clear the table first
        self.clearTable()
        # Execute query
        self.cur.execute(query)
        # Add columns to the table
        self.dbTable.setColumnCount(len(labels))
        # Set header labels
        self.dbTable.setHorizontalHeaderLabels(labels)
        # Set table title
        self.tableName.insert("Pokemon-Move-Version-Learn")

        inx = 0
        for row in self.cur.execute(query):
            self.dbTable.insertRow(inx)
            self.dbTable.setItem(inx, 0, QTableWidgetItem(str(row[0])))
            self.dbTable.setItem(inx, 1, QTableWidgetItem(str(row[1])))
            self.dbTable.setItem(inx, 2, QTableWidgetItem(str(row[2])))
            self.dbTable.setItem(inx, 3, QTableWidgetItem(str(row[3])))
            inx += 1

    def handlePokemonForms(self):
        query = "SELECT * FROM PokemonForm"
        labels = ["pokemonID", "formName"]
        self.handleTable(query, labels, "Pokemon-Forms")

    def handlePokemonTypes(self):
        query = "SELECT * FROM PokemonType"
        labels = ["pokemonID", "typeID", "slot"]
        self.handleTable(query, labels, "Pokemon-Types")

    def handleFormTypes(self):
        query = "SELECT * FROM FormType"
        labels = ["formName", "typeID", "slot"]
        self.handleTable(query, labels, "Pokemon-Types") 

    def handlePkmnHeldItemVrsn(self):
        query = "SELECT * FROM PkmnHeldItemVrsn"
        labels = ["pokemonID", "versionID", "itemID", "rarity"]
        self.handleTable(query, labels, "Pokemon-Items-Version")

    def handleMachines(self):
        query = "SELECT * FROM Machine"
        labels = ["machineNum", "vGroupID", "itemID", "moveID"]
        self.handleTable(query, labels, "Machines")

    def handlePkmnAreaVrsnEnc(self):
        query = "SELECT * FROM PkmnAreaVrsnEncntr"
        labels = ["versionID", "areaID", "eSlotID", "pokemonID"]
        # self.handleTable(query, labels, "Pokemon-Area-Version-Encounter")

        # Clear the table first
        self.clearTable()
        # Execute query
        self.cur.execute(query)
        # Add columns to the table
        self.dbTable.setColumnCount(len(labels))
        # Set header labels
        self.dbTable.setHorizontalHeaderLabels(labels)
        # Set table title
        self.tableName.insert("Pokemon-Area-Version-Encounter")

        inx = 0
        for row in self.cur.execute(query):
            self.dbTable.insertRow(inx)
            self.dbTable.setItem(inx, 0, QTableWidgetItem(str(row[0])))
            self.dbTable.setItem(inx, 1, QTableWidgetItem(str(row[1])))
            self.dbTable.setItem(inx, 2, QTableWidgetItem(str(row[2])))
            self.dbTable.setItem(inx, 3, QTableWidgetItem(str(row[3])))
            inx += 1
    
    def handlePokemonAbilities(self):
        query = "SELECT * FROM PkmnAbilities"
        labels = ["pokemonID", "abilityID", "isHidden", "slot"]
        self.handleTable(query, labels, "Pokemon-Abilities")

    def handlePokemonEggGroups(self):
        query = "SELECT * FROM PkmnEggGroup"
        labels = ["pokemonID", "eggGroupdID"]
        self.handleTable(query, labels, "Pokemon-EggGroup")

    def handleTable(self, query, labels, tableTitle):
        # Clear the table first
        self.clearTable()
        # Execute query
        self.cur.execute(query)
        # Fetch all rows
        rows = self.cur.fetchall()
        # Add columns to the table
        self.dbTable.setColumnCount(len(labels))
        # Set header labels
        self.dbTable.setHorizontalHeaderLabels(labels)
        # Set table title
        self.tableName.insert(tableTitle)

        for row in rows:
            inx = rows.index(row)
            self.dbTable.insertRow(inx)
            # Add the columns
            for col in range(len(labels)):
                self.dbTable.setItem(inx, col, QTableWidgetItem(str(row[col])))

    def clearTable(self):
        self.dbTable.setRowCount(0)
        self.tableName.clear()

    def initComboBox(self):
        alphabet = ["a","b","c","d","e",
                    "f","g","h","i","j",
                    "k","l","m","n","o",
                    "p","q","r","s","t",
                    "u","v","w","x","y",
                    "z"]
        self.comboBox.addItems(alphabet)

    def initRadBtns(self):
        self.weightGroup = QButtonGroup()
        self.weightGroup.addButton(self.heavyRad)
        self.weightGroup.addButton(self.lightRad)

        self.heavyRad.setChecked(True)
        
        self.statsGroup = QButtonGroup()
        self.statsGroup.addButton(self.highRad)
        self.statsGroup.addButton(self.lowRad)

        self.highRad.setChecked(True)

        self.numMovesGroups = QButtonGroup()
        self.numMovesGroups.addButton(self.mostRad)
        self.numMovesGroups.addButton(self.leastRad)

        self.mostRad.setChecked(True)

    
app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.showMaximized()
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")