package controller;

import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.control.Label;
import javafx.scene.control.Slider;
import javafx.scene.layout.*;
import javafx.util.Duration;
import javafx.animation.Animation;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.collections.ObservableList;
import javafx.fxml.Initializable;

import java.net.URL;
import java.util.ResourceBundle;

import model.GameOfLife;

/**
 * Implementation of the controller. Connects the view with the model.
 */
public class Controller implements Initializable {

   /**
    * Number of rows in the game grid.
    */
   private static final int ROWS = 30;

   /**
    * Number of columns in the game grid.
    */
   private static final int COLUMNS = 50;

   /**
    * Minimum size of a cell.
    */
   private static final int CELL_SIZE = 20;

   /**
    * Probability that a cell will be initialized as alive.
    */
   private static final double PROBABILITY = 0.35;

   /**
    * Slider for adjusting the animation speed.
    */
   @FXML
   private Slider speedSlider;

   /**
    * Label that displays the current generation.
    */
   @FXML
   private Label generationLabel;

   /**
    * GridPane containing Pane objects that represent the cells.
    */
   @FXML
   private GridPane gridPane;

   /**
    * GameOfLife model.
    */
   private GameOfLife gameofLife;

   /**
    * Timeline for the animation.
    */
   private Timeline timeline;

   /**
    * Initializes the JavaFX components.
    * This method is called after the FXML file has been loaded.
    *
    * @param url The location used to resolve relative paths for the root object, or null if the location is not known.
    * @param resourceBundle The resources used to localize the root object, or null if the root object was not localized.
    */
   @Override
   public void initialize(URL url, ResourceBundle resourceBundle) {
      gameofLife = new GameOfLife(ROWS, COLUMNS);

      timeline = new Timeline();
      timeline.setCycleCount(Timeline.INDEFINITE);
      timeline.getKeyFrames().addAll(new KeyFrame(Duration.seconds(1), (e -> {
         displayCellStatus();
         gameofLife.nextGeneration();
         setGenerationLabelText();
      })));

      speedSlider.valueProperty().addListener((observableValue, old_val, new_val) -> timeline.setRate(new_val.doubleValue()));

      for (int row = 0; row < ROWS; row++) {
         RowConstraints rowConst = new RowConstraints();
         rowConst.setPercentHeight(100.0 / ROWS);
         gridPane.getRowConstraints().add(rowConst);
      }

      for (int col = 0; col < COLUMNS; col++) {
         ColumnConstraints colConst = new ColumnConstraints();
         colConst.setPercentWidth(100.0 / COLUMNS);
         gridPane.getColumnConstraints().add(colConst);
      }

      for (int row = 0; row < ROWS; row++) {
         for (int col = 0; col < COLUMNS; col++) {
            Pane pane = new Pane();
            pane.setMinSize(CELL_SIZE, CELL_SIZE);
            pane.getStyleClass().add("cell");
            gridPane.add(pane, col, row);

            int finalRow = row;
            int finalCol = col;
            pane.setOnMouseClicked(event -> handleCellClick(finalRow, finalCol));
         }
      }
   }

   /**
    * Displays the status of each cell in the grid.
    * Cells are styled based on whether they are alive or dead.
    */
   private void displayCellStatus() {
      ObservableList<Node> cellNodes = gridPane.getChildren();
      for (Node node : cellNodes) {
         int row = GridPane.getRowIndex(node);
         int col = GridPane.getColumnIndex(node);

         node.getStyleClass().clear();
         node.getStyleClass().add("cell");
         if (gameofLife.isCellAlive(row, col)) {
            node.getStyleClass().add("alive-cell");
         }
      }
   }

   /**
    * Updates the generation label with the current generation number.
    */
   private void setGenerationLabelText() {
      int generation = gameofLife.getGeneration();
      String generationText = (generation == 1) ? "Generation" : "Generations";
      generationLabel.setText(String.format("%s: %d", generationText, generation));
   }

   /**
    * Starts the animation.
    * If the game is at the initial generation, it initializes the cells randomly.
    */
   public void play() {
      if (gameofLife.getGeneration() == 0) {
         gameofLife.initRandom(PROBABILITY, gameofLife);
      }
      if (Animation.Status.RUNNING != timeline.getStatus()) {
         timeline.play();
      }
   }

   /**
    * Pauses the animation.
    */
   public void pause() {
      if (Animation.Status.RUNNING == timeline.getStatus()) {
         timeline.pause();
      }
   }

   /**
    * Resets the game to the initial state.
    * Pauses the animation, resets the model, and updates the display.
    */
   public void reset() {
      timeline.pause();
      gameofLife.reset();
      generationLabel.setText("Generation: 0");
      displayCellStatus();
   }

   private void handleCellClick(int row, int col) {
      if (timeline.getStatus() != Animation.Status.RUNNING) {
         gameofLife.toggleCellState(row, col);
         displayCellStatus();
      }
   }
}
