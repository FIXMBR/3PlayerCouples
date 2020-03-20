class XMLError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class XML:
    def __init__(self, xml_file):
        self.filename = xml_file
        self.xml_contents = []
        self.attacks = []
        self.parse_xml(xml_file)

    def parse_xml(self, xml_file):
        try:
            xml_raw = open(xml_file, "rb").read()
        except:
            raise XMLError("Cannot open \"%s\"" % xml_file)

        # Convert to UNIX format
        xml_raw = xml_raw.replace(b"\r\n", b"\n")
        xml_raw = xml_raw.replace(b"\r", b"\n")

        
        xml_raw = xml_raw.decode()
        # Create params dictionary
        
        i = 0
        
        i = xml_raw.find("<ActorFrame", i)
        j = xml_raw.find("><children>", i+1)

        self.xml_contents.append(xml_raw[i:i+12])
        self.xml_contents.append(xml_raw[j:])
        

    

    def barf(self, LF="\r\n", mc=1, noteSkin="cybercouples", globalOffset=0.000):
        s = ""
        
        s+=self.xml_contents[0].replace("\n", "\r\n")
        s+=LF
        s+="InitCommand=\"%function(self)"+LF
        s+="offset = PREFSMAN:GetPreference('GlobalOffsetSeconds');"+LF

        for i in range(len(self.attacks)):
            (a, b, c) = self.attacks[i]
            s += "GAMESTATE:LaunchAttack(%.3f-offset,%.3f,'%s');" % (a, b, c) + LF
        
        s+="end\""+LF
        s+=self.xml_contents[1].replace("\n", "\r\n")
        return s

    # Static Methods

    @staticmethod
    def list_use_nums(ls):
        new = []
        for a, b in ls:
            new.append((float(a), float(b)))
        return new

