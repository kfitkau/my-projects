package model;

/**
 * Enumeration of the offsets of neighboring cells.
 * Each enum constant represents a direction relative to a cell: north, south, east, west, etc.
 */
public enum NeighbourDirection {
    NORTHWEST(-1, -1), // Offset for the northwest direction
    NORTH(0, -1),     // Offset for the north direction
    NORTHEAST(1, -1), // Offset for the northeast direction
    WEST(-1, 0),      // Offset for the west direction
    EAST(1, 0),       // Offset for the east direction
    SOUTHWEST(-1, 1), // Offset for the southwest direction
    SOUTH(0, 1),      // Offset for the south direction
    SOUTHEAST(1, 1);  // Offset for the southeast direction

    final int x; // X-coordinate offset
    final int y; // Y-coordinate offset

    /**
     * Constructor. Creates a new NeighbourDirection with the given x and y offsets.
     *
     * @param x X-coordinate offset.
     * @param y Y-coordinate offset.
     */
    NeighbourDirection(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
