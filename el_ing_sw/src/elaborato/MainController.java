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
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.text.Text;
import javafx.stage.Modality;
import javafx.stage.Stage;

public class MainController {
	//vari field
	@FXML
	TextField login;
	@FXML
	PasswordField password;
	@FXML
	Text risultato_login;
	@FXML
	Button Sign_in; //forse il problema del null-> @FXML
	
	@FXML
	private void controllo_credenziali(ActionEvent event) throws ClassNotFoundException, SQLException, IOException {
		System.out.println("prova");
		//risultato_login.setText("prova"); //mi da errore non so se serve qualche 
		
		//da inserire dopo il controllo delle credenziali *****
		//test
		Parent root = FXMLLoader.load(getClass().getResource("ric_ins.fxml"));
		
		Scene scene = new Scene(root);
		Stage primaryStage = new Stage();
		primaryStage.setTitle("Ricerca/Inserimento");
		primaryStage.setScene(scene);
		//specifico la modalità della nuova finestra
		primaryStage.initModality(Modality.WINDOW_MODAL);
		primaryStage.initOwner(Sign_in.getScene().getWindow()); //specifica il proprietario della nuova finestra; mi da problemi
		primaryStage.show();
		
		//se dovessi prendere dei valori da un private dovrei creare i metodi pubblici get oppure per invirare set
		
		//controlla nella base di stai se le credenziali esistono e sono corrette
		
		/*
		//richiesta driver
		Class.forName("org.postgresql.Driver");
		
		//creazione connessione
		Connection con = DriverManager.getConnection(null);
		
		//creazione statement; usato per la creazione di query
		Statement st= con.createStatement();
		
		//cursore sulla tebella risultato
		ResultSet rs= st.executeQuery(
				"SELECT ca.login, ca.pw FROM credenziali_accesso ca");
		
		//controllo le credenziali
		while(rs.next()) {
			//controllo che il login e la password siano corrette
			if(rs.getString("login") == login.getText()) {
				if(rs.getString("pw") == password.getText()) {
					//potrei mettere una varianìbile che se true mi manda avanti nell'interfacci
					//oppure se le credenziali sono presenti mi apre una nuova finestra per l'inserimento o la ricerca
					********
					*Parent root = FXMLLoader.load(getClass().getResource("ric_ins.fxml"));
		
					Scene scene = new Scene(root);
					Stage primaryStage = new Stage();
					primaryStage.setTitle("Ricerca/Inserimento");
					primaryStage.setScene(scene);
					//specifico la modalità della nuova finestra
					primaryStage.initModality(Modality.WINDOW_MODAL);
					//primaryStage.initOwner(Sign_in.getScene().getWindow()); //specifica il proprietario della nuova finestra; mi da problemi
					primaryStage.show();
				}
				else
					System.out.println("password errata\n");
			}
		}
		//mettere un controllo per dire che il login è errato
		con.close();*/
	}
	
	public void initialize(URL url, ResourceBundle resources){
		// TODO Auto-generated constructor stub
	}
	

}
