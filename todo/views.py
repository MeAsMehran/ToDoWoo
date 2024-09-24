from django.shortcuts import render , redirect , get_object_or_404          # adding redirect for ?????     # get_object_or_404 for finding an object by using a pk number

# UserCreationForm: THIS IS FOR CREATING FORMS LIKE SIGNUP(NAME, PASSWORD, CONFIRM PASSWORD)(IT PROVIDES US A READY FORM)
# AuthenticationForm: THIS IS FOR CREATING A LOGIN FORM (NAME, PASSWORD YOU SET)(IT PROVIDES US A READY FORM)
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm

from django.contrib.auth.models import User             # THIS IS FOR CREATING A NEW USER
from django.db.utils import IntegrityError              # Add this import statement at the top of the file

# login: This helps us after we sign up with a user name, we login to the site with that user.
# logout: This helps us after we logged in with a username , can logout as a user
# authenticate: This helps us to have access user's name and password which signed up in the site. By importing this we can check if the entry name and password is correct or not.
from django.contrib.auth import login , logout , authenticate
from django.utils import timezone

from .forms import ToDoForm     # we imported the forms file to use it here
from .models import todo

# This allows only currently logged-in users or only a user that is logged in to access a particular view. for example if we log out from
# aiBlog.html and refresh it we still can see the page
# which is bad(only logged-in user should see this page). so
# we add a library to check that. (1:49:21 in Youtube video)
from django.contrib.auth.decorators import login_required

# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')


def signupuser(request):
    form = UserCreationForm()   # creating a signup form (name, password, confirm password)
    
    if request.method == 'GET':
        return render(request, 'Signup.html', {'form':form})    #for dictionary we could do this: {'form':UserCreationForm()}
    else:
        # create a new user
        if request.POST['password1'] == request.POST['password2']:      # we got these password1 and password2 and username below by inspecting(inspect) the page which contains the sign up form.
            try:    # this try except will check if the username is already signed up or not
                
                # for creating a user we need to import User from django.contrib.auth.models
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])  # you can get username and password1 variable names like we did in chrome, if you go to sign up page and inspect the page you see the variables in html codes.
                # remember to certain the arguments in User.create_user() variable name => username=request.POST['username'], password=...
                
                user.save() # we get the user info now we should save the user data to database
                login(request, user)    # login with the user we signed up
                return redirect('userTodosPage')  # You should give currentTodo url(name='currentTodo') which you set in url.py
                
            # return render(request, 'Signup.html', {'form':form})
            except IntegrityError:
                return render(request, 'Signup.html', {'form':form,'error': 'That username has already been taken .Please choose a new username'})
        else:
            # tell the user passwords didn't match
            error = "Passwords doesn't match"
            return render(request, 'Signup.html', {'form':form,'error': error})



# if @login_required set on top of a certain method that method needs a logged-in user to work!
@login_required     # this will let only a logged-in user can have access to this page
def logoutuser(request):
    # the reason that we want to check if the request is POST or not is that
    # most browsers are loading all the <a> tags before we click to the link.
    # so if we have a <a> tag defined as logout in html file we will
    # logged out the as soon as we log in to the page because all
    # <a> tags are GET requests so check if request was POST log me out:
    if request.method == 'POST':
        logout(request)
        # welcome here is the function we define the top of this file and related to path('')
        return redirect('welcomePage')  # what if we used return render(request, 'welcome.html')?????????


def loginuser(request):     # kinda similar to signup method
    form = AuthenticationForm   # creating a login form(name, password)
    
    if request.method == 'GET':
        return render(request, 'Loginuser.html', {'form':form})    #for dictionary we could do this: {'form':UserCreationForm()}
    else:
        # this will check if the username is available and if yes, the password is correct or not.
        # If the username was available and password was correct(conditions), it will
        # return a user with with these username and password and if those 2 conditions were wrong, it will return a None.
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'Loginuser.html', {'form':form, 'error':'Username and pasword did not match!'})
        else:
            login(request, user)
            return redirect('userTodosPage')


# if @login_required set on top of a certain method that method needs a logged-in user to work!
@login_required     # this will let only a logged-in user can have access to this page
def userTodos(request):
    # todos = todo.objects.all()      # in here we get all the todos (even other users' todos) which is bad, we only want user to see their own todos
    # todos = todo.objects.filter(user=request.user)  # this will show users their own todos instead of all users' todos
    todos = todo.objects.filter(user=request.user, targetDate__isnull=True)     # targetDate__isnull=True: we can filter task which is done by using targetDate field models.py file, if targetDate has a value it wont be shown and if it dont have a value it would be shown
    return render(request, 'userTodos.html', {'todos': todos})



# if @login_required set on top of a certain method that method needs a logged-in user to work!
@login_required     # this will let only a logged-in user can have access to this page
def createToDo(request):
    if request.method == 'GET':
        
        # we created a file and named it form.py and then define a form there for users to fill their task and info in there(which is ToDoForm())
        # and then we import that file in views.py and pass the form as dictionary here
        return render(request, 'createTodo.html', {'form': ToDoForm()})
    else:
        try:        # this try and except is for bad given data like having a long title name or something like that
            form = ToDoForm(request.POST)   # getting the data from request.POST(the info that user entered) and info we entered from the ToDoForm() and give them to form variable
            newtodo = form.save(commit=False)   # commit=False: creating a new object and DONT NECESSARILY SAVE IT TO DATA BASE
            newtodo.user = request.user     # we specify the user field here, so we dont create a todo for another user
            newtodo.save()                  # save the info into data base
            return redirect('userTodosPage')
        except ValueError:
            return render(request, 'createTodo.html', {'form': ToDoForm(), 'error': 'bad data passed in. Try again'})



# if @login_required set on top of a certain method that method needs a logged-in user to work!
@login_required     # this will let only a logged-in user can have access to this page
def view_todo(request, todo_pk):

    # For finding an object we can use primary key(any created object has a special key number for accessing)
    # user=request.user: not only we need and primary key as an object key or id to get it we also need to know if that object belongs to a specific user(so the only user which can see the object is the current logged in user(request.user) and can see only own objects or tasks not others). The reason we are doing this is a user don't have access to other users object by giving the object id to browser search bar
    # get_object_or_404 should be imported (from django.shortcuts import get_object_or_404) for finding an object
    # get_object_or_404(models.py class name, pk= , user=request.user)
    userTodo = get_object_or_404(todo, pk=todo_pk, user=request.user)  # this only shows the info and we can't change the data

    if request.method == 'GET':
        # We fill the form with the object's data. The reason we are using form in here is because we can modify object data like title or memo in forms(editing task)
        form = ToDoForm(instance=userTodo)  # instance=userTodo: instance will fill the form with the data we got after finding the object

        return render(request, 'selectedTodo.html', {'userTodo': userTodo, 'form': form})
    else:
        try:
            form = ToDoForm(request.POST, instance=userTodo)    # instance=userTodo: this will help it know that this is a existing object we are trying to update
            form.save()
            return redirect('userTodosPage')
        except ValueError:
            return render(request, 'selectedTodo.html', {'userTodo': userTodo, 'form': form, 'error': "Bad Info"})


# if @login_required set on top of a certain method that method needs a logged-in user to work!
@login_required     # this will let only a logged-in user can have access to this page
def complete_todo(request, todo_pk):
    # First we get the usertodo object
    usertodo = get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        # Then we set the task time as timezone.now()
        usertodo.targetDate = timezone.now()
        usertodo.save()     # we save the task's or object's changes
        return redirect('userTodosPage')



# if @login_required set on top of a certain method that method needs a logged-in user to work!
@login_required     # this will let only a logged-in user can have access to this page
def delete_todo(request, todo_pk):
    usertodo = get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        usertodo.delete()
        return redirect('userTodosPage')



# if @login_required set on top of a certain method that method needs a logged-in user to work!
@login_required     # this will let only a logged-in user can have access to this page
def undo_completed_todo(request, todo_pk):
    usertodo = get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        try:
            usertodo.targetDate = None
            usertodo.save()
            return redirect('completedTodosPage')
        except ValueError:
            return render(request, 'completedTodos.html', {'error': "error"})


# if @login_required set on top of a certain method that method needs a logged-in user to work!
@login_required     # this will let only a logged-in user can have access to this page
def completed(request):
    # todos = todo.objects.filter(user=request.user, targetDate__isnull=False)      # getting all the objects created by user which are completed
    todos = todo.objects.filter(user=request.user, targetDate__isnull=False).order_by('-targetDate')    # .order_by('targetDate') shows the tasks sorted by targetDate and - means lately done tasks shows above than the rest
    return render(request, 'completedTodos.html', {'todos': todos})








