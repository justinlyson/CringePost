import xml.etree.ElementTree as XML
from pathlib import Path
import os


def timeToString(sec):
    hour = int(sec / (60 * 60))
    minute = int((sec / 60) % 60)
    second = int(sec % 60)
    return str(hour) + '-' + str(minute) + '-' + str(second)


class TwitchVideo:
    def __init__(self, twitchId):
        self.twitchId = twitchId
        self.fps = 0
        self.quality = ""
        self.videoPath = ""
        self.streamer = "_"
        self.length = 0
        self.editTime = 0
        self.downloadTime = 0

    def videoName(self):
        return self.streamer + '_' + self.twitchId + ".mp4"

    def deleteVideo(self):
        os.remove(self.videoPath + "\\" + self.videoName())


class YoutubeVideo:
    def __init__(self, twitchVideo):
        self.twitchVideo = twitchVideo
        self.hero = ""
        self.videoPath = twitchVideo.videoPath
        self.gameNumber = ""
        self.description = ""
        self.tags = ""
        self.keywords = ""
        self.startSecond = 0
        self.lastSecond = 0
        self.skip = False
        self.skipReason = ""
        self.editTime = 0
        self.uploadTime = 0

    def videoFileName(self):
        return self.hero + '_' + timeToString(self.startSecond) + '=' + timeToString(
            self.lastSecond) + '_' + self.twitchVideo.twitchId + ".mp4"

    def videoTitle(self):
        name = self.twitchVideo.streamer
        champion = self.hero
        gameNumber = self.gameNumber
        return name + " " + champion + "#" + str(gameNumber) + " Full Gameplay  Season 7"

    def toString(self):
        return self.videoTitle()

    def populateData(self):
        configFile = Path(str(self.videoPath) + "\\config.xml")
        xmlTree = XML.parse(configFile)
        xmlRoot = xmlTree.getroot()

        # All Videos ID's we have Recorded
        youtubeElement = xmlRoot.find('youtube')
        tagElement = youtubeElement.find("tags")
        tagsElements = tagElement.findall("tag")

        tagString = ""
        for tag in tagsElements:
            tagString += tag.get("text") + " , "
        tagString = tagString[:-3]
        self.tags = tagString
        self.keywords = self.tags

        descriptionElement = youtubeElement.find("description")
        self.description = descriptionElement.text

        herosElement = xmlRoot.find('heros')
        heroElement = herosElement.find(self.hero)

        if heroElement is None:
            self.gameNumber = 1
            XML.SubElement(herosElement, self.hero, {'count': "2"})
        else:
            self.gameNumber = int(heroElement.get("count"))
            heroElement.set('count', str(self.gameNumber + 1))

        xmlTree.write(str(configFile))

    def deleteVideo(self):
        os.remove(self.videoPath + "\\" + self.videoFileName())
