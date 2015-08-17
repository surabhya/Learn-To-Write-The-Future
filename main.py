import webapp2
import jinja2
import os
import json
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class HomePage(Handler):
    def get(self):
         self.render("index.html")

class Help(Handler):
    def get(self):
        self.render("help.html")

class Quotes(db.Model):
    title = db.StringProperty(required = True)
    URL = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class AddQuotes(Handler):

    def get(self):
        self.render("addquotes.html")

    def error(self, title, URL, password, done, error):
        self.render("addquotes.html", title=title, url=URL, password=password, done_add_quotes=done, error_add_quotes=error)
        
    def post(self):
        title = self.request.get("title").strip()
        URL = self.request.get("url").strip()
        password = self.request.get("password")
        if (password=="#Devil"):
            if URL:
                if not("http" in URL):
                    error = "URL doesnot exist"
                    self.error(title, URL, "", "", error)
                elif title:
                    a = Quotes(title = title, URL = URL)
                    a.put()
                    done = "Quote has been updated"
                    self.render("addquotes.html" ,title="", url="", password="", done_add_quotes=done, error_add_quotes="")  
                else:
                    error = "Add Title"
                    self.error(title, URL, "", "", error)
            else:
                error = "Add required infromation"
                self.error(title, URL, "", "", error)
        elif (password==""):
            error = "Enter password"
            self.error(title, URL, "", "", error)
        else:
            error = "Password mismatch"
            self.error(title, URL, "", "", error)
            

class DisplayQuotes(Handler):
    def get(self):
        contents = db.GqlQuery("SELECT * FROM Quotes ORDER BY created DESC limit 10")
        contents = list(contents)
        self.render("displayquotes.html", contents = contents)

class Images(db.Model):
    title = db.StringProperty(required = True)
    URL = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class AddImages(Handler):

    def get(self):
        self.render("addimages.html")

    def error(self, title, URL, password, done, error):
        self.render("addimages.html", title=title, url=URL, password=password, done_add_images=done, error_add_images=error)
        
    def post(self):
        title = self.request.get("title").strip()
        URL = self.request.get("url").strip()
        password = self.request.get("password")
        if (password=="#Devil"):
            if URL:
                if not("http" in URL):
                    error = "URL doesnot exist"
                    self.error(title, URL, "", "", error)
                elif title:
                    a = Images(title = title, URL = URL)
                    a.put()
                    done = "Image has been updated"
                    self.render("addimages.html" ,title="", url="", password="", done_add_images=done, error_add_images="")  
                else:
                    error = "Add Title"
                    self.error(title, URL, "", "", error)
            else:
                error = "Add required infromation"
                self.error(title, URL, "", "", error)
        elif (password==""):
            error = "Enter password"
            self.error(title, URL, "", "", error)
        else:
            error = "Password mismatch"
            self.error(title, URL, "", "", error)
            

class DisplayImages(Handler):
    def get(self):
        contents = db.GqlQuery("SELECT * FROM Images ORDER BY created DESC limit 10")
        contents = list(contents)
        self.render("displayimages.html", contents = contents) 

class Videos(db.Model):
    Type = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    URL = db.StringProperty(required = True)
    time = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class AddVideos(Handler):

    def get(self):
        self.render("addvideos.html")

    def error(self, title, URL, time, Type, error):
        self.render("addvideos.html", title=title, url=URL, time=time, typee = Type , password="", done_add_videos="", error_add_videos=error)
    
    def time_valid(self, time):
        if not(":" in time):
            return False
        else:
            time_list = time.split(":")
            if len(time_list)== 2:
                return (time_list[0].isdigit() and time_list[1].isdigit())
            else:
                return False 

    def post(self):
        title = self.request.get("title").strip()
        URL = self.request.get("url").strip()
        Type = self.request.get("typee").lower().strip()
        time = self.request.get("time").strip()
        password = self.request.get("password")
        if (password=="#Devil"):
            if not( title and URL and Type and time):
                error = "Add all the infromation before submitting"
                self.error(title, URL, time, Type, error)
            elif not (Type == "featured" or Type=="inspirational" or Type == "playlist"):
                error = "Type correct type"
                self.error(title, URL, time, "", error)
            elif not("embed" in URL or "playlist" in URL):
                error = "Enter the embed url"
                self.error(title, "", time, Type, error)
            elif not(time):
                error = "Enter time"
                self.error(title, URL, "", Type, error)
            elif not(self.time_valid(time)):
                error = "Enter time in correct format"
                self.error(title, URL, "" ,Type, error)
            else:
                delete(section="Videos", Type=Type)
                a = Videos(Type = Type, title = title, URL = URL, time = time)
                a.put()
                done = "Video has been updated"
                return self.render("addvideos.html" ,title="", url="", typee="", time="", done_add_videos=done, error_add_videos="")
        elif (password==""):
            error = "Enter password"
            self.error(title, URL, time, Type, error)
        else:
            error = "Password mismatch"
            self.error(title, URL, time, Type, error)
            

class DisplayVideos(Handler):
    def get(self):
        contents = db.GqlQuery("SELECT * FROM Videos ORDER BY created DESC limit 10")
        contents = list(contents)
        self.render("displayvideos.html", contents = contents) 

def delete(title = "", URL= "", section="", Type=""):
    if section.lower() == "videos" and Type:
        q = db.GqlQuery("SELECT * FROM Videos Where Type=" + "'" + Type +"'")
        results = q.fetch(1000)
        while results:
            db.delete(results)
            results = q.fetch(1000, len(results))
    elif section.lower() == "quotes" and URL:
        q = db.GqlQuery("SELECT * FROM Quotes Where URL=" + "'" + URL +"'")
        results = q.fetch(1000)
        while results:
            db.delete(results)
            results = q.fetch(1000, len(results))
    elif section.lower() == "quotes" and title:
        q = db.GqlQuery("SELECT * FROM Quotes Where title=" + "'" + title +"'")
        results = q.fetch(1000)
        while results:
            db.delete(results)
            results = q.fetch(1000, len(results))
    elif section.lower() == "images" and URL:
        q = db.GqlQuery("SELECT * FROM Images Where URL=" + "'" + URL +"'")
        results = q.fetch(1000)
        while results:
            db.delete(results)
            results = q.fetch(1000, len(results))
    elif section.lower() == "images" and title:
        q = db.GqlQuery("SELECT * FROM Images Where title=" + "'" + title +"'")
        results = q.fetch(1000)
        while results:
            db.delete(results)
            results = q.fetch(1000, len(results))

class Delete(Handler):

    def get(self):
        self.render("deletepage.html")

    def post(self):
        title = self.request.get("title").strip()
        URL = self.request.get("url").strip()
        section = self.request.get("section").lower().strip()
        password = self.request.get("password")
        if (password=="#Devil"):
            if not( (title or URL) and section):
                error = "Add the required infromation before submitting"
                self.render("deletepage.html", title=title, url=URL, section = section , password="", done_delete="", error_delete=error)
            elif not (section == "images" or section =="quotes"):
                self.render("deletepage.html" ,title=title, url=URL, section="",done_delete="", password="", error_delete="Type correct section")
            elif URL:
                if not("http" in URL or "www" in URL):
                    self.render("deletepage.html" ,title=title, url="", section=section, password="", done_delete="", error_delete="Enter the correct url")
                else:
                    delete(title=title, URL=URL, section = section)
                    done = section.capitalize() + " has been updated"
                    self.render("deletepage.html" ,title="", url="", section="", password="", done_delete=done, error_delete="")

            else:
                delete(title=title, URL=URL, section = section)
                done = section.capitalize() + " has been deleted"
                self.render("deletepage.html" ,title="", url="", section="", password="", done_delete=done, error_delete="")
        elif (password==""):
            error = "Enter password"
            self.render("deletepage.html", title=title, url=URL, section=section , password="", done_delete="", error_delete=error)
        else:
            error = "Password mismatch"
            self.render("deletepage.html", title=title, url=URL, section=section , password="", done_delete="", error_delete=error)

class DisplayQuotesJson(Handler):
    
    def get(self):
         contents = db.GqlQuery("SELECT * FROM Quotes ORDER BY created DESC")
         json_list = []
         for c in contents:
             dic = {}
             dic['title'] = c.title
             dic['URL'] = c.URL
             dic['created'] = "" + str(c.created)
             json_list.append(dic)
         x = json.dumps(json_list)
         self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
         self.write(x)

class DisplayImagesJson(Handler):
    
    def get(self):
         contents = db.GqlQuery("SELECT * FROM Images ORDER BY created DESC")
         json_list = []
         for c in contents:
             dic = {}
             dic['title'] = c.title
             dic['URL'] = c.URL
             dic['created'] = "" + str(c.created)
             json_list.append(dic)
         x = json.dumps(json_list)
         self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
         self.write(x)

class DisplayVideosJson(Handler):
    
    def get(self):
         contents = db.GqlQuery("SELECT * FROM Videos ORDER BY Type")
         json_list = []
         for c in contents:
             dic = {}
             dic['Type'] = c.Type
             dic['title'] = c.title
             dic['URL'] = c.URL
             dic['time'] = c.time
             dic['created'] = "" + str(c.created)
             json_list.append(dic)
         x = json.dumps(json_list)
         self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
         self.write(x)

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/help', Help),
    ('/addquotes', AddQuotes),
    ('/displayquotes', DisplayQuotes),
    ('/displayquotes.json', DisplayQuotesJson),
    ('/addimages', AddImages),
    ('/displayimages', DisplayImages),
    ('/displayimages.json', DisplayImagesJson),
    ('/addvideos', AddVideos),
    ('/displayvideos', DisplayVideos),
    ('/displayvideos.json', DisplayVideosJson),
    ('/delete', Delete)
], debug=True)
