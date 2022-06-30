package elaborato;

import java.io.IOException;
import java.net.URL;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ResourceBundle;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.text.Text;
import javafx.stage.Modality;
import javafx.stage.Stage;

public class ins_ric_controller{
	@FXML
	Button ricerca;
	@FXML
	Button inserimento;
	
	@FXML
	private void ricerca_finestra(ActionEvent event) throws IOException {
		Parent root = FXMLLoader.load(getClass().getResource("ricerca.fxml"));
		
		Scene scene = new Scene(root);
		Stage primaryStage = new Stage();
		primaryStage.setTitle("Ricerca");
		primaryStage.setScene(scene);
		//specifico la modalità della nuova finestra
		primaryStage.initModality(Modality.WINDOW_MODAL);
		primaryStage.initOwner(ricerca.getScene().getWindow()); //specifica il proprietario della nuova finestra; mi da problemi
		primaryStage.show();
	}
	
	@FXML
	private void inserimento_finestra(ActionEvent event) throws IOException {
		Parent root = FXMLLoader.load(getClass().getResource("inserimento.fxml"));
		
		Scene scene = new Scene(root);
		Stage primaryStage = new Stage();
		primaryStage.setTitle("Inserimento");
		primaryStage.setScene(scene);
		//specifico la modalità della nuova finestra
		primaryStage.initModality(Modality.WINDOW_MODAL);
		primaryStage.initOwner(inserimento.getScene().getWindow()); //specifica il proprietario della nuova finestra; mi da problemi
		primaryStage.show();
	}
	
	public void initialize(URL arg0, ResourceBundle arg1) {
		// TODO Auto-generated method stub
		
	}

}
