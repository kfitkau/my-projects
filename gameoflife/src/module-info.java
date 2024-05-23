module GameOfLife
{
   exports controller;

   exports application;

   requires javafx.base;

   requires javafx.controls;

   requires javafx.fxml;

   requires transitive javafx.graphics;

   opens controller;
}