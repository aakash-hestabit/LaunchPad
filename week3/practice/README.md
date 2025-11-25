# WEEK 3 
## ScreenShots
### Login Page

This is the login page. I have implemented a middleware that checks the user's login status on every route request. It checks whether the user is logged in by verifying if the username is stored in the local storage. If the user is not logged in, they are redirected to the login page.

| **For Larger Screens** | **For Mobile Screens** |
| ---------------------- | ---------------------- |
| ![login page](image.png) | ![mobile screen](image-2.png) |

Here is how the user's info is stored in the local storage:

| **Local Storage Info** |
| ---------------------- |
| ![localstorage](image-1.png) |

After login, the user is redirected to the home page.

---

### Home/Landing Page

| **For Larger Screens** | **For Mobile Screens** |
| ---------------------- | ---------------------- |
| ![landing page](image-3.png) | ![landing page](image-4.png) |

---

### Dashboard

From the sidebar, the user can navigate to the dashboard. In the header, the user can navigate to the profile page. On the dashboard, I have displayed various cards for different purposes, along with area and bar charts.

The cards are rendered using a reusable component, and the popup modal that appears when clicking on the card button is also rendered using a reusable component. Each popup modal takes button-specific details.

| **For Larger Screens** | **For Mobile Screens** |
| ---------------------- | ---------------------- |
| ![dashboard for larger screens](image-5.png) | ![dashboard on mobile screens](image-7.png) |
| ![pop up modal for buttons](image-6.png) | ![pop up modal for screens](image-8.png) |

---

### Sidebar and Dynamic Routing

In the sidebar, I used some routes, and based on that, I implemented dynamic routing for the layout and the pages dropdown.

| **Dynamic Routes in VS Code** |
| ---------------------------- |
| ![dynamic routes](image-10.png) |

Here, I have destructured the parameters and extracted the params array:

| **Destructuring Params and Extracting Values** |
| --------------------------------------------- |
| ![destructuring params and extracting values](image-11.png) |

---

### Users Listing Page

This is the users listing page for larger screens. Each page shows some details using the reusable popup details.

| **For Larger Screens** | **For Mobile Screens** |
| ---------------------- | ---------------------- |
| ![users page](image-12.png) | ![users listing for mobile](image-14.png) |
| ![pop up modal for user listing](image-13.png) | ![pop up modal for smaller screens](image-15.png) |

---

### Profile Page

This is the profile page for larger screens.

| **For Larger Screens** | **For Smaller Screens** |
| ---------------------- | ----------------------- |
| ![profile page](image-16.png) | ![smaller screens](image-17.png) |

---




## DAY 1 
 on day 1 i learned the nextjs basics and fundamentals, how to create components in nextjs , how nextjs has file based routing and how can we create some private folders inside the app directory which are not served as routes. also i learned how layout is applied to the children.Along with this i learned how we can group the routes.
 Then i made a navbar whic had the logo for site and a searchbar with a button to redirect the user to profile page using the `Link` tag, there i came to know how next js optimizes the navigation, while using the `<Link> </Link>` tag it prefetches the data when the link is visible to viewport or is hovered.

