
# Part 4: Advanced JavaScript Topics for Front-End Developer Interview

## 9. React Lifecycle Methods

React lifecycle methods are used to control what happens during the different phases of a component’s lifecycle: mounting, updating, and unmounting.

### Mounting Phase:
1. **constructor()**: Called when the component is initialized.
2. **render()**: Returns the JSX that the component will display.
3. **componentDidMount()**: Called after the component is rendered. Good for API calls.

### Updating Phase:
1. **shouldComponentUpdate()**: Determines if the component should re-render based on changes in props or state.
2. **componentDidUpdate()**: Invoked after the component is re-rendered.

### Unmounting Phase:
1. **componentWillUnmount()**: Called just before the component is destroyed. Useful for cleaning up resources such as timers.

### Example of Lifecycle Methods:
```javascript
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }

  componentDidMount() {
    console.log('Component mounted');
  }

  componentDidUpdate(prevProps, prevState) {
    console.log('Component updated');
  }

  componentWillUnmount() {
    console.log('Component will unmount');
  }

  render() {
    return <div>Count: {this.state.count}</div>;
  }
}
```

### Hooks Equivalent:
With React hooks, lifecycle methods are handled with `useEffect()`.
```javascript
import React, { useEffect } from 'react';

function MyComponent() {
  useEffect(() => {
    console.log('Component mounted');
    return () => {
      console.log('Component will unmount');
    };
  }, []);

  return <div>Hello!</div>;
}
```

---

## 10. Event Handling in React

Event handling in React is similar to handling DOM events, but with a few key differences.

### Example of an Event Handler in React:
```javascript
function MyButton() {
  const handleClick = () => {
    alert('Button clicked!');
  };

  return <button onClick={handleClick}>Click me</button>;
}
```

### Differences from DOM Event Handling:
1. **CamelCase Syntax**: React uses camelCase for event names (`onClick` instead of `onclick`).
2. **Synthetic Events**: React wraps native events in its own wrapper called SyntheticEvent, providing cross-browser compatibility.
3. **Event Binding**: In class components, event handlers need to be bound to the class instance.

---

## 11. Virtual DOM

The **Virtual DOM** is a concept where a virtual representation of the UI is kept in memory. React compares this virtual representation with the actual DOM (called **reconciliation**) and updates only the changed parts.

### Why Use Virtual DOM?
- **Efficiency**: Directly manipulating the DOM is expensive. React minimizes the amount of DOM manipulation needed.
- **Reconciliation**: React calculates the most efficient way to update the real DOM based on changes in the virtual DOM.

### Example:
```javascript
const element = <h1>Hello, world!</h1>;
ReactDOM.render(element, document.getElementById('root'));
```

When the state or props change, React updates the virtual DOM and only re-renders the changed parts, avoiding full page re-renders.

---
