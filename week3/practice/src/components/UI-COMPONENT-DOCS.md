# UI COMPONENTS USAGE DOCS 

## The Card Component
I have made Card as a reusable component which can be used differently each time different props are passed to it , 
`const Card = ({height='120px',width='310px',label='Default Label',details='This is the default text for details',color ='red', handleModalOpen=''})`
as ypu can see that it takes multiple props which include height, width, label, details and color . incase i do not want to pass props this component accept default proprs also which are specified above. using different props we can render different cards with diffrent informaton. also this component is used along with the popup modal and hence accepts a `handleModalOpen` function that handles the closing of the popup modal as the name suggests,

## The PopUp ModalComponent 
this component is also reusable and accepts props `const Modal = ({handleModalClose,modalDetails})`. So it takes two props, one is handleModalClose that is a function which will be called when closing the modal by clicking the cross button or outside the information card. The other prop is the modalDetails, this is the information that will be displayed by the modal. by passing these two props we can use this modal differently everytime.