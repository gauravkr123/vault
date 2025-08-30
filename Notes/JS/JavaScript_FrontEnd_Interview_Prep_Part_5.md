
# Part 5: Advanced JavaScript Topics for Front-End Developer Interview

## 12. Context API in React

The Context API in React is a way to pass data through the component tree without having to pass props down manually at every level. It is useful for managing global state, such as user authentication or theme settings.

### Example of Using Context:
1. **Create a Context**:
```javascript
const ThemeContext = React.createContext('light');
```

2. **Provide the Context**: Wrap a part of the component tree with a `Provider`.
```javascript
function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}
```

3. **Consume the Context**: Access the context value in any component.
```javascript
function Toolbar() {
  return (
    <div>
      <ThemeButton />
    </div>
  );
}

function ThemeButton() {
  const theme = React.useContext(ThemeContext);
  return <button className={theme}>Button with {theme} theme</button>;
}
```

### When to Use Context:
- Context is useful when data needs to be shared across many components without prop-drilling (passing props through every component layer). 
- It is ideal for things like themes, user authentication, or any global settings.

---

## 13. React Router

React Router is a library used to handle routing in a React application. It allows you to map different URLs to specific components, enabling single-page applications (SPA) with dynamic navigation.

### Key Features:
- **Declarative Routing**: Routes are defined as components.
- **Dynamic Routing**: Components are rendered based on the current URL.
- **History API**: Uses the browser's history API to manage navigation.

### Example of Basic Routing:
```javascript
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/about">About</Link></li>
          </ul>
        </nav>

        <Switch>
          <Route path="/" exact><Home /></Route>
          <Route path="/about"><About /></Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home() {
  return <h2>Home</h2>;
}

function About() {
  return <h2>About</h2>;
}
```

### Route Parameters:
React Router also supports dynamic route parameters.
```javascript
<Route path="/user/:id" component={User} />
function User({ match }) {
  return <h2>User ID: {match.params.id}</h2>;
}
```

### Nested Routes:
```javascript
function Topics() {
  return (
    <div>
      <h2>Topics</h2>
      <Switch>
        <Route path="/topics/:topicId"><Topic /></Route>
        <Route path="/topics"><h3>Please select a topic.</h3></Route>
      </Switch>
    </div>
  );
}
```

---

## 14. Webpack

**Webpack** is a module bundler that compiles JavaScript modules (along with CSS, images, etc.) into a bundle to be served in the browser. It helps optimize the performance of web applications by bundling and minifying files.

### Key Features:
- **Entry Point**: The starting point for Webpack to build its internal dependency graph.
- **Loaders**: Enable Webpack to process other types of files, such as CSS, images, or TypeScript.
- **Plugins**: Add extra functionality, such as optimizing bundles or injecting environment variables.

### Basic Webpack Configuration:
```javascript
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
};
```

### Key Terms:
- **Tree Shaking**: Removes unused code to reduce bundle size.
- **Code Splitting**: Breaks the bundle into smaller chunks to improve load performance.

---

## 15. Babel

**Babel** is a JavaScript compiler used to convert modern JavaScript (ES6+) into a backwards-compatible version that can run in older browsers.

### Why Babel?
Browsers do not always support the latest JavaScript features (e.g., arrow functions, classes). Babel helps by converting these features into an older JavaScript syntax.

### Example of Babel Config (`.babelrc`):
```json
{
  "presets": ["@babel/preset-env", "@babel/preset-react"]
}
```

### Common Babel Presets:
- **@babel/preset-env**: Transforms ES6+ syntax into ES5.
- **@babel/preset-react**: Transforms JSX into JavaScript.

Babel works in conjunction with Webpack to compile modern JavaScript code and enable cross-browser compatibility.
