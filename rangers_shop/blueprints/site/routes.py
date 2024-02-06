from flask import Blueprint, render_template 



# need to instantiate our Blueprint class
#instantiate our Blueprint class

                                     #location of html files
site = Blueprint('site', __name__, template_folder='site_templates') # = is the keyword argument to jump to, 'site_templates' is location of html files

# use site object to create our routes
@site.route('/')
def shop():
    return render_template('shop.html') # looking inside our template_folder (site_templates) to find our shop.html file