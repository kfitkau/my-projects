package model;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Class representing a cell.
 * This class holds information about the state of a cell and its neighboring cells.
 */
public class Cell {

   /**
    * Indicates whether the cell is alive.
    */
   private boolean alive;

   /**
    * Contains the neighboring cells and their statuses.
    */
   private final Map<Cell, Boolean> neighbouringCells;

   /**
    * Constructor. Creates a new cell with the given initial state.
    *
    * @param alive Initial cell state.
    */
   public Cell(boolean alive) {
      this.alive = alive;
      neighbouringCells = new HashMap<>();
   }

   /**
    * Constructor. Creates a new dead cell.
    */
   public Cell() {
      this(false);
   }

   /**
    * Returns the current state of the cell.
    *
    * @return true if the cell is alive, false if the cell is dead.
    */
   public boolean isAlive() {
      return alive;
   }

   /**
    * Sets the state of the cell to the given value.
    *
    * @param alive true if the cell is alive, false if the cell is dead.
    */
   public void setAlive(boolean alive) {
      this.alive = alive;
   }

   /**
    * Adds a neighboring cell to the cell.
    *
    * @param neighbour Neighboring cell.
    */
   public void addNeighbour(Cell neighbour) {
      neighbouringCells.put(neighbour, neighbour.isAlive());
   }

   /**
    * Updates the states of neighboring cells.
    */
   public void updateNeighbours() {
      for (Cell neighbour : neighbouringCells.keySet()) {
         neighbouringCells.replace(neighbour, neighbour.isAlive());
      }
   }

   /**
    * Calculates the next state of the cell and returns the set of affected neighboring cells.
    *
    * @return Set of neighboring cells affected by the state change.
    */
   public Set<Cell> nextState() {
      boolean nextState = calculateNextState();
      Set<Cell> affectedCells = new HashSet<>();
      if (alive != nextState) {
         alive = nextState;
         affectedCells.addAll(neighbouringCells.keySet());
      }
      return affectedCells;
   }

   /**
    * Calculates the next state of the cell based on the game rules.
    *
    * @return true if the cell should be alive in the next generation, false otherwise.
    */
   private boolean calculateNextState() {
      long aliveNeighbours = countAliveNeighbours();
      return alive && aliveNeighbours == 2 || aliveNeighbours == 3;
   }

   /**
    * Counts the number of alive neighboring cells.
    *
    * @return Number of alive neighboring cells.
    */
   private long countAliveNeighbours() {
      return neighbouringCells.values().stream().filter(Boolean::booleanValue).count();
   }
}