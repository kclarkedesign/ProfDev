Endpoints:

/api/users
/auth/users/me/
/token/login/

/api/menu-items/
/api/menu-items/{menuItem}

/api/groups/manager/users/
/api/groups/manager/users/{userId}

/api/groups/delivery-crew/users/
/api/groups/delivery-crew/users/{userId}

/api/cart/menu-items/

/api/orders/
/api/orders/{orderId}


##Grading Criteria Overview
When you submit your assignment, other learners in the course will review and grade your work. These are the criteria they’ll use to evaluate your APIs.

In this project, your APIs need to make it possible for your end-users to perform certain tasks and your reviewer will be looking for the following functionalities.

1. The admin can assign users to the manager group

2. You can access the manager group with an admin token

3. The admin can add menu items

4. The admin can add categories

5. Managers can log in

6. Managers can update the item of the day

7. Managers can assign users to the delivery crew

8. Managers can assign orders to the delivery crew

9. The delivery crew can access orders assigned to them

10. The delivery crew can update an order as delivered

11. Customers can register

12. Customers can log in using their username and password and get access tokens

13. Customers can browse all categories

14. Customers can browse all the menu items at once

15. Customers can browse menu items by category

16. Customers can paginate menu items

17. Customers can sort menu items by price

18. Customers can add menu items to the cart

19. Customers can access previously added items in the cart

20. Customers can place orders

21. Customers can browse their own orders

You'll also need to give feedback on and grade the assignments of two other learners using the same criteria.

##How to review your peers

Once you have submitted your file, you are required to review two peer submissions. You can view the peers that you need to review in the “Peers to review” section. You need to download their zipped project folder and unzip it. Then, prepare the virtual environment and install all dependencies using the following commands.

cd LittleLemon

pipenv shell

pipenv install

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

Then log into the Django admin panel and create superuser and user groups and randomly assign them into these groups, the same way you did in your own project.
