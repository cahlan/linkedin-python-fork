import datetime

from xml.dom import minidom
from xml.sax.saxutils import unescape

def get_child(node, tagName):
    try:
        domNode = node.getElementsByTagName(tagName)[0]
        childNodes = domNode.childNodes
        if childNodes:
            return childNodes[0].nodeValue
        return None
    except:
        return None

def str_to_bool(s):
    if s.lower() == "true":
        return True
    elif s.lower() == "false":
        return False
    else:
        return None

def parse_date(node):
    year = int(get_child(node, "year"))
    month = get_child(node, "month")
    if month:
        month = int(month)
    else:
        month = 1
    return datetime.date(year, month, 1)

def parse_connections(connections_node):
    connections_list = []
    connections = connections_node.getElementsByTagName("connection")
    if connections:
        for connection in connections:
            person = connection.getElementsByTagName("person")
            if person:
                person = person[0]
                connections_list.append(Profile.create(person))

    return connections_list

class LinkedInModel:
    
    def __repr__(self):
        d = {}
        for x,y in self.__dict__.items():
            if (self.__dict__[x]):
                d[x] = y
        return (self.__module__ + "." + self.__class__.__name__ + " " +
                d.__repr__())
        
class Publication(LinkedInModel):

    def __init__(self):
        self.id = None
        self.title = None
        self.publisher_name = None
        self.date = None
        self.url = None
        self.summary = None
        # Notice that we are ignoring authors field for now until someone will need it.

    @staticmethod
    def create(node):
        """
        <publication>
            <id>3</id>
            <title>Publication list, with links to individual papers</title>
            <publisher>
                <name>Iftach</name>
            </publisher>
            <date>
                <year>2005</year>
                <month>5</month>
            </date>
            <url>URLURL</url>
            <summary>My summary</summary>
        </publication>
        """
        publication = Publication()
        publication.id = get_child(node, "id")
        publication.title = get_child(node, "title")

        publisher = node.getElementsByTagName("publisher")
        if publisher:
            publication.publisher_name = get_child(publisher[0], "name")
        
        date = node.getElementsByTagName("date")
        if date:
            publication.date = parse_date(date[0])

        publication.url = get_child(node, "url")
        publication.summary = get_child(node, "summary")
        return publication

class Company(LinkedInModel):

    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.size = None
        self.industry = None
        self.ticker = None

    @staticmethod
    def create(node):
        """
        <company>
        <id>1009</id>
        <name>XIV - IBM</name>
        <type>Public Company</type>
        <size>123</size>
        <industry>Information Technology and Services</industry>
        <ticker>IBM</ticker>
        </company>
        """
        company = Company()
        company.id = get_child(node, "id")
        company.name = get_child(node, "name")
        company.type = get_child(node, "type")
        company.size = get_child(node, "size")
        company.industry = get_child(node, "industry")
        company.ticker = get_child(node, "ticker")
        return company

class Education(LinkedInModel):
    """
    Class that wraps an education info of a user
    """
    def __init__(self):
        self.id          = None
        self.school_name = None
        self.degree      = None
        self.start_date  = None
        self.end_date    = None
        self.activities  = None
        self.notes       = None
        self.field_of_study = None
        
    @staticmethod
    def create(node):
        """
        <educations total="">
         <education>
          <id>
          <school-name>
          <degree>
          <start-date>
           <year>
          </start-date>
          <end-date>
           <year>
          </end-date>
         </education>
        </educations>
        """
        children = node.getElementsByTagName("education")
        result = []
        for child in children:
            education = Education()
            education.id = education._get_child(child, "id")
            education.activities = education._get_child(child, "activities")
            education.notes = education._get_child(child, "notes")
            education.school_name = education._get_child(child, "school-name")
            education.degree = education._get_child(child, "degree")
            education.field_of_study = education._get_child(child, "field-of-study")

            start_date = child.getElementsByTagName("start-date")
            if start_date:
                education.start_date = parse_date(start_date[0])
                
            end_date = child.getElementsByTagName("end-date")
            if end_date:
                education.end_date = parse_date(end_date[0])

            result.append(education)            
        return result
    
    def _get_child(self, node, tagName):
        try:
            domNode = node.getElementsByTagName(tagName)[0]
            childNodes = domNode.childNodes
            if childNodes:
                return childNodes[0].nodeValue
            return None
        except:
            return None

class Position(LinkedInModel):
    """
    Class that wraps a business position info of a user
    """
    def __init__(self):
        self.id         = None
        self.title      = None
        self.summary    = None
        self.start_date = None
        self.end_date   = None
        self.company    = None
        self.is_current = None
        

    @staticmethod
    def create(node):
        """
         <position>
          <id>101526695</id>
          <title>Developer</title>
          <summary></summary>
          <start-date>
          <year>2009</year>
          <month>9</month>
          </start-date>
          <is-current>true</is-current>
          <company>
            <name>Akinon</name>
          </company>
         </position>
        """
        position = Position()
        position.id = get_child(node, "id")
        position.title = get_child(node, "title")
        position.summary = get_child(node, "summary")
        position.is_current = str_to_bool(get_child(node, "is-current"))

        company = node.getElementsByTagName("company")
        if company:
            position.company = Company.create(company[0])

        start_date = node.getElementsByTagName("start-date")
        if start_date:
            position.start_date = parse_date(start_date[0])

        end_date = node.getElementsByTagName("end-date")
        if end_date:
            position.end_date = parse_date(end_date[0])

        return position
        
class Location(LinkedInModel):
    def __init__(self):
        self.name = None
        self.country_code = None
        
    @staticmethod
    def create(node):
        """
        <location>
            <name>
            <country>
                <code>
            </country>
        </location>
        """
        loc = Location()
        loc.name = get_child(node, "name")
        country = node.getElementsByTagName("country")
        if country:
            country = country[0]
            loc.country_code = get_child(country, "code")
            
        return loc
    
class RelationToViewer(LinkedInModel):
    def __init__(self):
        self.distance = None
        self.num_related_connections = None
        self.connections = []
        
    @classmethod
    def create(cls, node):
        """
        <relation-to-viewer>
            <distance>1</distance>
            <connections total="36" count="10" start="0">
                <connection>
                    <person>
                        <id>_tQbzI5kEk</id>
                        <first-name>Michael</first-name>
                        <last-name>Green</last-name>
                    </person>
                </connection>
            </connections>
        </relation-to-viewer>
        """
        relation = RelationToViewer()
        relation.distance = int(get_child(node, "distance"))
        relation.num_related_connections = int(get_child(node, "num-related-connections"))
        
        connections = node.getElementsByTagName("connections")
        if connections:
            connections = connections[0]
            if not relation.num_related_connections:
                if connections.hasAttribute("total"):
                    relation.num_related_connections = int(connections.attributes["total"].value)

            relation.connections = parse_connections(connections)
                    
        return relation
    
class Profile(LinkedInModel):
    """
    Wraps the data which comes from Profile API of LinkedIn.
    For further information, take a look at LinkedIn Profile API.
    """
    def __init__(self):
        self.id          = None
        self.first_name  = None
        self.last_name   = None
        self.headline    = None
        self.location    = None
        self.industry    = None
        self.distance    = None
        self.relation_to_viewer = None
        self.summary     = None
        self.specialties = None
        self.proposal_comments = None
        self.associations = None
        self.interests   = None
        self.honors      = None
        self.public_url  = None
        self.private_url = None
        self.picture_url = None
        self.current_status = None
        self.current_share = None
        self.num_connections = None
        self.num_connections_capped = None
        self.languages   = []
        self.skills      = []
        self.connections = []
        self.positions   = []
        self.educations  = []
        self.xml_string  = None
        
    @staticmethod
    def create(node, debug=False):
        person = node
        if person.nodeName != "person":
            person = person.getElementsByTagName("person")[0]
        profile = Profile()
        profile.id = get_child(person, "id")
        profile.first_name = get_child(person, "first-name")
        profile.last_name = get_child(person, "last-name")
        profile.headline = get_child(person, "headline")
        profile.distance = get_child(person, "distance")
        profile.specialties = get_child(person, "specialties")
        profile.proposal_comments = get_child(person, "proposal-comments")
        profile.associations = get_child(person, "associations")
        profile.industry = get_child(person, "industry")
        profile.honors = get_child(person, "honors")
        profile.interests = get_child(person, "interests")
        profile.summary = get_child(person, "summary")
        profile.picture_url = profile._unescape(get_child(person, "picture-url"))
        profile.current_status = get_child(person, "current-status")
        profile.current_share = get_child(person, "current-share")
        profile.num_connections = get_child(person, "num-connections")
        profile.num_connections_capped = get_child(person, "num-connections-capped")
        profile.public_url = profile._unescape(get_child(person, "public-profile-url"))

        location = person.getElementsByTagName("location")
        if location:
            profile.location = Location.create(location[0])

        relation_to_viewer = person.getElementsByTagName("relation-to-viewer")
        if relation_to_viewer:
            relation_to_viewer = relation_to_viewer[0]
            profile.relation_to_viewer = RelationToViewer.create(relation_to_viewer)

        # Create connections
        connections = person.getElementsByTagName("connections")
        if connections:
            connections = connections[0]
            if not profile.num_connections and connections.hasAttribute("total"):
                profile.num_connections = int(connections.attributes["total"].value)
            profile.connections = parse_connections(connections)

        # create positions
        positions = person.getElementsByTagName("positions")

        if positions:
            positions = positions[0]
            positions = positions.getElementsByTagName("position")
            # TODO get the total
            for position in positions:
                profile.positions.append(Position.create(position))

        # TODO Last field working on is - publications

        private_profile = person.getElementsByTagName("site-standard-profile-request")
        if private_profile:
            private_profile = private_profile[0]
        profile.private_url = get_child(private_profile, "url")

        # create skills
        skills = person.getElementsByTagName("skills")
        if skills:
            skills = skills[0]
            children = skills.getElementsByTagName('skill')
            for child in children:
                if not child.getElementsByTagName('id'):
                    profile.skills.append(get_child(child, 'name'))

        # create languages
        languages = person.getElementsByTagName("languages")
        if languages:
            languages = languages[0]
            children = languages.getElementsByTagName('language')
            for child in children:
                if not child.getElementsByTagName('id'):
                    profile.languages.append(get_child(child, 'name'))

        # create educations
        educations = person.getElementsByTagName("educations")
        if educations:
            educations = educations[0]
            profile.educations = Education.create(educations)

        # For debugging
        if debug:
            profile.xml_string = node.toxml()

        return profile

    def _unescape(self, url):
        if url:
            return unescape(url)
        return url

class Update(LinkedInModel):
    """
    Wraps data, added by Cahlan Sharp
    """
    def __init__(self):
      self.id             = None
      self.user_id        = None
      self.user_firstname = None
      self.user_lastname  = None
      self.user_headline  = None
      self.type           = None
      self.current_status = None
      self.picture_url    = None
      self.num_likes      = None
      self.timestamp      = None
      self.profile_url    = None

    @staticmethod
    def create(xml_string):
      print "creating update from string"
      print xml_string
      try:
        document = minidom.parseString(xml_string)            
        update = document.getElementsByTagName("update")[0]
        nupdate = Update()
        nupdate.id = nupdate._get_child(update, "update-key")
        nupdate.type = nupdate._get_child(update, "update-type")
        nupdate.num_likes = nupdate._get_child(update, "num-likes")
        nupdate.timestamp = nupdate._get_child(update, "timestamp")
        content = update.getElementsByTagName("update-content")
        if content:
          content = content[0]
          pcontent = content.getElementsByTagName("person")
          if pcontent:
            content = pcontent[0]
            nupdate.user_id = nupdate._get_child(content, "id")
            nupdate.user_firstname = nupdate._get_child(content, "first-name")
            nupdate.user_lastname = nupdate._get_child(content, "last-name")
            nupdate.user_headline = nupdate._get_child(content, "headline")
            share_req = content.getElementsByTagName("current-share")
            if share_req:
              share_req = share_req[0]
              nupdate.current_status = nupdate._get_child(share_req, "comment")
            nupdate.picture_url = nupdate._get_child(content, "picture-url")
            profile_req = content.getElementsByTagName("api-standard-profile-request")
            if profile_req:
              profile_req = profile_req[0]
              nupdate.profile_url = nupdate._get_child(profile_req, "url")

          return nupdate
      except:
        return None

      return None

    def _unescape(self, url):
      if url:
        return unescape(url)
      return url

    def _get_child(self, node, tagName):
        try:
            if tagName == "summary":
                for n in node.getElementsByTagName(tagName):
                    if n.parentNode.tagName == node.tagName:
                        domNode = n
                        break
            else:
                domNode = node.getElementsByTagName(tagName)[0]

            if domNode.parentNode.tagName == node.tagName:
                childNodes = domNode.childNodes
                if childNodes:
                    return childNodes[0].nodeValue
                return None
            else:
                return None
        except:
            return None


