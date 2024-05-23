package model;

import javafx.scene.input.MouseButton;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

/**
 * Implementation of Conway's Game of Life.
 * This class represents the game board and provides methods to initialize, update, and query the state of cells.
 */
public class GameOfLife {

   /**
    * Number of rows in the game grid.
    */
   private final int rows;

   /**
    * Number of columns in the game grid.
    */
   private final int columns;

   /**
    * Current generation count.
    */
   private int generation;

   /**
    * Array of cells representing the game board.
    */
   private final Cell[][] cellGrid;

   /**
    * Set of cells whose status needs to be recalculated.
    */
   private Set<Cell> affectedCells;

   /**
    * Constructor. Creates a new GameOfLife object with the specified number of rows and columns.
    *
    * @param rows    Number of rows in the game grid.
    * @param columns Number of columns in the game grid.
    */
   public GameOfLife(int rows, int columns) {
      if (rows <= 0 || columns <= 0) {
         throw new IllegalArgumentException("Invalid number of rows or columns!");
      }

      this.rows = rows;
      this.columns = columns;
      generation = 0;
      cellGrid = new Cell[rows][columns];
      affectedCells = new HashSet<>();

      // Initialize cells and their neighbors
      for (int row = 0; row < rows; row++) {
         for (int col = 0; col < columns; col++) {
            cellGrid[row][col] = new Cell();
         }
      }
      connectNeighbours();
   }

   /**
    * Initializes the state of cells randomly with the given probability.
    *
    * @param probability Probability that a cell is alive initially.
    */
   public void initRandom(double probability, GameOfLife gameofLife) {
      if (probability <= 0 || probability > 1.0) {
         throw new IllegalArgumentException("Invalid probability value!");
      }

      Random random = new Random();
      for (int row = 0; row < rows; row++) {
         for (int col = 0; col < columns; col++) {
            if (gameofLife.isCellAlive(row, col)) {
               cellGrid[row][col].setAlive(true);
            } else {
               cellGrid[row][col].setAlive(random.nextDouble() <= probability);
            }
            affectedCells.add(cellGrid[row][col]);
         }
      }
      updateNeighbours();
   }

   /**
    * Calculates the next generation of cells based on the game rules.
    */
   public void nextGeneration() {
      Set<Cell> affectedCellsNextGeneration = new HashSet<>();
      for (Cell cell : affectedCells) {
         affectedCellsNextGeneration.addAll(cell.nextState());
      }
      updateNeighbours();
      affectedCells = affectedCellsNextGeneration;
      generation++;
   }

   /**
    * Resets the game state.
    */
   public void reset() {
      for (int row = 0; row < rows; row++) {
         for (int col = 0; col < columns; col++) {
            cellGrid[row][col].setAlive(false);
         }
      }
      updateNeighbours();
      affectedCells.clear();
      generation = 0;
   }

   /**
    * Returns the current generation count.
    *
    * @return Current generation count.
    */
   public int getGeneration() {
      return generation;
   }

   /**
    * Checks if the cell at the specified row and column is alive.
    *
    * @param row Row index of the cell.
    * @param col Column index of the cell.
    * @return true if the cell is alive, false otherwise.
    */
   public boolean isCellAlive(int row, int col) {
      return cellGrid[row][col].isAlive();
   }

   /**
    * Connects each cell to its neighbors.
    */
   private void connectNeighbours() {
      for (int row = 0; row < rows; row++) {
         for (int col = 0; col < columns; col++) {
            Cell cell = cellGrid[row][col];
            for (NeighbourDirection direction : NeighbourDirection.values()) {
               int nCol = col + direction.x;
               int nRow = row + direction.y;
               if (isValidCell(nRow, nCol)) {
                  Cell neighbour = cellGrid[nRow][nCol];
                  cell.addNeighbour(neighbour);
               }
            }
         }
      }
   }

   /**
    * Updates the neighbors of all cells.
    */
   private void updateNeighbours() {
      for (int row = 0; row < rows; row++) {
         for (int col = 0; col < columns; col++) {
            cellGrid[row][col].updateNeighbours();
         }
      }
   }

   /**
    * Checks if the given row and column are valid cell indices.
    *
    * @param row Row index.
    * @param col Column index.
    * @return true if the indices are valid, false otherwise.
    */
   private boolean isValidCell(int row, int col) {
      return row >= 0 && row < rows && col >= 0 && col < columns;
   }

   /**
    * Toggles the state of a cell at the specified row and column when clicked with the mouse.
    *
    * @param row      Row index of the cell.
    * @param col      Column index of the cell.
    */
   public void toggleCellState(int row, int col) {
      if (isValidCell(row, col)) {
         Cell cell = cellGrid[row][col];
         cell.setAlive(!cell.isAlive());
      }
   }
}
