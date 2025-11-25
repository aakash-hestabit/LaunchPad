# UI COMPONENTS USAGE DOCS

## The Card Component
I have made Card as a reusable component which can be used differently each time different props are passed to it.

`const Card = ({height='120px',width='310px',label='Default Label',details='This is the default text for details',color ='red', handleModalOpen=''})`

As you can see, it takes multiple props which include height, width, label, details and color. In case I do not want to pass props, this component accepts default props also which are specified above. Using different props we can render different cards with different information. Also this component is used along with the popup modal and hence accepts a `handleModalOpen` function that handles opening the popup modal as the name suggests.

---

## The PopUp Modal Component
This component is also reusable and accepts props:

`const Modal = ({handleModalClose,modalDetails})`

So it takes two props, one is `handleModalClose` that is a function which will be called when closing the modal by clicking the cross button or by clicking outside the information card.  
The other prop is the `modalDetails`, this is the information that will be displayed inside the modal. By passing these two props we can use this modal differently everytime.

---

## The Button Component
This is a simple reusable button component:

`const Button = ({title, handleClick,color="white", background = "gray", height="50px", width="200px", radius="rounded-lg"})`

It takes multiple props for customizing the button like text color, background color, height, width and the border radius.  
If no props are passed, the button will use the default props mentioned above.  
This button also accepts a `handleClick` function which will run whenever the button is clicked.  
Using these props we can create different types of buttons for different needs.

---

## The ChartCard Component
This component is used to display charts inside a card layout:

`const ChartCard = ({ title, logo, children })`

It takes three props:  
- `title` to show the name of the chart  
- `logo` to show any icon or symbol  
- `children` which will be the actual chart

By passing different charts as children, we can reuse the same card structure for any type of chart.

---

## The FeatureCard Component
This is a reusable card to show small information sections:

`const FeatureCard = ({ title, description })`

It accepts two props which are `title` and `description`.  
Both of these props are displayed inside a styled card layout.  
By changing the title and description, we can use this card anywhere to show simple feature blocks.

---

## The TestimonialCard Component
This component is used to display user or client testimonials:

`const TestimonialCard = ({ text, name, title })`

It accepts three props:  
- `text` which is the testimonial message  
- `name` which is the user's name  
- `title` which is the user's profession or role  

By passing different values we can display different testimonials using the same card layout.

---

