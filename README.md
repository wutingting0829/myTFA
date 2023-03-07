# Strong two-factor biometric module development_v2

### 2023/2/18 
* new database for comment system `blog\models.py` and `blog\admin.py`
* create form for comments
    * django has the facility. we just tell it what model or field we want to use and it will automatically make a form for us.
    * 因為我用的是boostraps套件，所以多命名一個widget方法。
* Build the comments functionality - view.py　
    * grabbing the data from table `blog\forms.py`
    * to extend the `single.html` view to also include the comments. so, we just need to extend the post_single funcion. `blog\views.py`
    * change single.html `blog\templates\single.html`

### 2023/2/19 - 2/20 - buiding a simple category system for an existing blog application
> * Models(foreign key)
> * Using Class based generic view
> * Model queries/filters
> * Custom temolate processors
> * Category pages/Menu dropdown

* Build the category model
    1. build some categories
    2. create connection (foreign key between the post table and category table) `blog\models.py`
* Developing the view
    1. bulid a category page: we can see a specific post from a specific category. `blog\views.py`
    2. [Built-in class-based generic views](https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-display/) 
    3. we're gonna generate a new class-based view to extract the information from the database that's relevant to the URL. `blog\views.py`
    4. Add new URL `blog\urls.py`
    5. if your screen didn't show any catlist
    ![](https://i.imgur.com/7J7dlrT.png)
    please check your category name all be lower case.
    ![](https://i.imgur.com/lJfQAEY.png)
* Template processors - develop drop-down menu
    * build new category_list `blog\views.py`
    * add new setting `blog.views.category_list` in `mysite\seetings.py`

### 2023/2/22-25 User Authentication System
* Activating Django Authentication
    * add new path for account `mysite\urls.py`
* Django Authentication Template Folder
    * add new folder `templates\registation\login.html`
    * define where your templates folded to reside --> using OS from python and we're going to join these two paths, so we going to request the base directory from django for our project and we're going to create a new folder which we've already done call templates. `mysite\settings.py -- TEMPLATES=[
    'DIRS': [os.path.join(BASE_DIR,'templates')],]`

* Templates for the project 
    * adding the content of other pages inside of this bolck here `templates\base\base.html`
    * a footer file `templates\base\footer.html`
    * a navigation file `templates\base\nav-main.html`
        * the css that's building the user profile in login page

* Building an initial login.html page
    * using existing form: representing the login form `templates\registration\login.html` 
    * add csrf token
    * extending the login form

* create a new account app dedicated to user account features 
    * extend form/ authentication logic
        * create a new app `accounts` --> `py manage.py startapp accounts` 
        * add new apps in `settings.py`
        
    * futher develop account model
        * want to overwrite some of these urls `path('account/', include('accounts.urls', namespace='accounts')),`
        * inital `accounts\urls.py`
        
            ```
            from django.urls import path
            from . import views
            app_name = 'accounts'
            urlpatterns = []`
           ```
* Building a custom login page / form
    * `\accounts\froms.py`
        * to be utilizing widgets , extending and adding our own attributes
        
        ```
        username = forms.CharField(widget=forms.TimeInput(attrs={'class': 'form-contorl mb-3', 'placeholder':'Username', 'id': 'login-username'}))
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-contorl', 'placeholder':'Password', 'id': 'login-pwd'}))
        ```
    * url - point it to our new form
        * `acccounrs\urls.py`
        * overwriting and overweiting the user login form `authentication_form=UserLoginForm` : the user login form resprents the form that we just created and the `authentication_form` repersents the previous authenticaiton form
    * update form - `templates\registration\login.html` template

* Building the Profile page / Dashboard page
    * create `templates\accounts\profile.html` : this is the page where is the authenticated users will land on when it login 
    * to create a view for this profile, because i want to ensure that only authenticated users can access this view  `accounts\urls.py` 
    * to build the view for the profile page `accounts\views.py`
    * correct the login redierct `mysite\settings.py`
* Developing the registration system with email confirmation
    * register.html
    * custom form
    * custom view - with email confirmation
* Developing the registration system with email confirmation
    * create a new html `templates\registration\register.html`
    * user completes registration form `accounts\forms.py`
    * email sent `mysite\settings.py` --> `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
    * user clicks to confirm `registration\account_activation_email.html`
    * create a `accounts\token.py`
    * account is activated `accounts\urls.py` --> `templates\registration\register.html`
        * we include the `accounts:activate` in `account_activaion_email.html`, so need to add in `urls.py` to utlize that 
        * create activate function in `accounts\views.py`
        * create a new html to `return render(request, 'registration/activation_invalid.html')` in `templates\registration\activation_invalid.html`
    
* Building the logging out feature: when someone logs out to get them sent to the login page
    * redirect to login
    * `templates\registration\logged_out.html`
* Building the forgotten password  / reset feature
    * user can use the email to reset the password `accounts\forms.py` --> `accounts\urls.py`
    * password_reset_form.html
    * password_reset_email.html
    * password_reset_done.html
    * password_reset_confirm.html
    * password_reset_complete.html
*  Building the User Profile Update feature
    * user can edit there detail informs `update.html`
    *  creaete user ediet form in `accounts\forms.py` --> `accounts\urls.py`
    *  add edit function in custom view `accounts\views.py`
*  Building the User Password change - for logged in users
    *  create new function in `accounts\forms.py` --> `accounts\urls.py`
    *  password_change_form.html
    *  password_change_done.html
*  Building the Delete user feature
    *  delete.html
    *  create new function in `accounts\views.py` --> `accounts\urls.py`
* image source : https://picsum.photos/images#2  
 
