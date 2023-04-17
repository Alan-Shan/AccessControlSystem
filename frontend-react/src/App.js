import './App.css';
import NavigationBar from "./components/NavigationBar";
import RouterView from "./router";

function App() {
  return (
      <div id="app">
        <NavigationBar />
        <RouterView />
        </div>
  );
}

export default App;
