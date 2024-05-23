package application;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.control.ButtonType;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.scene.control.Alert;

/**
 * Main class for the JavaFX application.
 * This class serves as the entry point for the Game of Life application.
 */
public class Main extends Application {

   /**
    * The main entry point for all JavaFX applications.
    * This method is called after the application is initialized.
    * It configures and displays the primary application window.
    *
    * @param primaryStage The primary stage for this application, onto which
    * the application scene can be set.
    */
   @Override
   public void start(Stage primaryStage) {
      try {
         BorderPane root = FXMLLoader.load(Main.class.getResource("/GameOfLife.fxml"));
         Scene scene = new Scene(root);

         primaryStage.setTitle("Game of Life");
         primaryStage.getIcons().addAll(
                 new Image(getClass().getResource("/icon_16x16.png").toString()),
                 new Image(getClass().getResource("/icon_32x32.png").toString()),
                 new Image(getClass().getResource("/icon_64x64.png").toString())
         );
         primaryStage.setScene(scene);
         primaryStage.sizeToScene();
         primaryStage.show();
         primaryStage.setMinWidth(primaryStage.getWidth());
         primaryStage.setMinHeight(primaryStage.getHeight());
      } catch (Exception e) {
         Alert alert = new Alert(Alert.AlertType.ERROR, e.getMessage(), ButtonType.OK);
         alert.showAndWait();
      }
   }

   /**
    * The main method, which serves as the entry point for the program.
    * Launches the JavaFX application.
    *
    * @param args Command line arguments.
    */
   public static void main(String[] args) {
      launch(args);
   }
}
