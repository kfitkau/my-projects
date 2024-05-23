<a name="readme-top"></a>

<br />
<div align="center">

<h3 align="center">Conway's Game of Life - JavaFX Implementation</h3>

  <p align="center">
    Welcome to the GitHub repository for my JavaFX implementation of Conway's Game of Life! This project visually simulates the cellular automaton devised by mathematician John Conway. I'm using SceneBuilder for the interface design. The application features play, pause, and reset buttons, allowing users to control the simulation's progress easily. Users can observe the evolution of the cell grid over time according to Conway's rules of birth, death, and survival.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a JavaFX implementation of Conway's Game of Life! It's using SceneBuilder for the interface design. The application features play, pause, and reset buttons, allowing users to control the simulation's progress easily. Users can observe the evolution of the cell grid over time according to Conway's rules of birth, death, and survival. The Game of Life, created by mathematician John Horton Conway in 1970, is a cellular automaton that functions as a zero-player game. Its progression depends solely on its initial configuration, with no additional input required. The game's grid is an infinite, two-dimensional array of square cells, each of which can be either alive or dead. The state of each cell is influenced by its eight neighboring cells. The evolution of the grid follows four rules: a living cell with fewer than two or more than three live neighbors dies, a living cell with two or three live neighbors survives, and a dead cell with exactly three live neighbors becomes alive. These rules are applied simultaneously to all cells to form each new generation. The Game of Life is Turing complete, capable of simulating any Turing machine, making it a powerful computational model.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Java Openjdk-22.0.1](https://jdk.java.net/22/)
* [JavaFX 17.0.11 SDK](https://gluonhq.com/products/javafx/)
* [SceneBuilder](https://gluonhq.com/products/scene-builder/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
### Prerequisites

Git: For cloning the repository.\
OpenJDK 22.0.1: Java Development Kit.\
JavaFX 17.0.11 SDK: JavaFX libraries.

### Installation
Step 1: Clone the Repository

1. Open a terminal or command prompt.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command
```git
git clone https://github.com/kfitkau/my-projects.git
```
For this Project you only need the folder "GameOfLife"

Step 2: Set Up the JavaFX SDK
1. Download the [JavaFX 17.0.11 SDK](https://gluonhq.com/products/javafx/) from the Gluon website.
2. Extract the downloaded SDK to a directory of your choice.

```diff
@@ If you want to use your Development Environment follow Step 3a, if you want to use the jar follow Step 3b! @@
```

Step 3a: Set Up Your Development Environment
For IntelliJ IDEA:
1. Open IntelliJ IDEA and select Open to open the folder "GameOfLife" of the cloned repository.
2. Configure JDK:
   * Go to File > Project Structure > Project.
   * Set the Project SDK to OpenJDK 22.0.1. If it’s not listed, add it by clicking New... and navigating to the JDK installation directory.
3. Add JavaFX Libraries:
   * Go to File > Project Structure > Libraries.
   * Click on + and select Java.
   * Navigate to the lib directory of the JavaFX SDK and select all the .jar files.
   * Apply the changes.
4. Add VM Options:
   * Go to Run > Edit Configurations.
   * Select your run configuration.
   * In the VM options field, add the following:
     ```
     --module-path /your/path/to/javafx-sdk-17.0.11/lib --add-modules javafx.controls,javafx.fxml,javafx.graphics,javafx.base
     ```
     Replace /path/to/javafx-sdk-17.0.11 with the actual path to the extracted JavaFX SDK.

Step 3b:
1. Install OpenJDK 22.0.1
   * Windows/Mac/Linux: Download OpenJDK 22.0.1 from the [official website](https://jdk.java.net/22/) and follow the installation instructions for your operating system.
   * Verify the installation by running:
     ```
     java -version
     ```
2. Open a terminal and cd to "your/path/to/GameOfLife/out/artifacts/GameOfLife_jar"
3. Use the following command template to run the JAR file
   ```
   java --module-path /your/path/to/javafx-sdk-17.0.11/lib --add-modules javafx.controls,javafx.fxml,javafx.graphics,javafx.base -jar gameoflife.jar
   ```
   Replace /path/to/javafx-sdk-17.0.11/lib with the actual path to the lib directory of your JavaFX SDK

Step 4: Run Your Application
* Make sure all dependencies and libraries are properly set up.
* Run your application from your IDE.
* Your JavaFX application should now launch, utilizing OpenJDK 22.0.1 and JavaFX 17.0.11.

Troubleshooting
* Class Not Found: Ensure that the JavaFX libraries are correctly added to your project.
* Module Path Issues: Double-check the VM options for the correct module path and module names.
* Build Issues: Ensure your project structure and dependencies are correctly configured.
By following these steps, you should be able to clone the GitHub repository and set up your JavaFX project successfully.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage
* Start/Pause: Begin or halt the simulation.
* Clear Grid: Reset the grid to an empty state.
* Adjust Speed: Control the evolution speed of the simulation.
* Click on "Cell" to remove it or to add a new Cell.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

If you encounter any issues during installation or usage, refer to the project's documentation or GitHub repository for troubleshooting tips.<br/>
Make sure to check for any specific configuration options or environment variables that might be required for the application to run smoothly.<br/>
This guide assumes a basic setup. For advanced usage or customization, consult the project's source code.

### Resources
[Game Of Life Wiki](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>