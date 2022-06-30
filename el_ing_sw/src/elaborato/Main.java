package elaborato;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Scene;

public class Main extends Application{
	
	@Override
	public void start(Stage primaryStage){
		// TODO Auto-generated method stub
		Scene scene;
		FXMLLoader loader = new FXMLLoader(getClass().getResource("ing_sw.fxml"));/*creare*/
		
		try {
			scene = new Scene(loader.load()); //il bottone mi da problemi; invalid identifier fx:id il nome non deve avere spazzi
			primaryStage.setScene(scene);
			primaryStage.show();
		} catch(Exception e) {
			e.printStackTrace();
		}
	}

	
	public static void main(String[] args) {
		
		//scena fxml
		launch(args);
		
		//login dipendente
		
		
		 //connesione al server (richiesta driver e connesione)
		
		//posso scrivere la base di dati in xml??
		
		//dipendenti dell'azienda
		/*dipendente:
		 *dati anagrafici
		 * indirizzo email
		 * telefono
		 * credenziali di accesso (login e password)
		 */
		
		//inserire i dati del lavoratore
		//simil ER
		/*lavoratore:
		 * 
		 * nome,cognome,luogo e data di nascita, nazionalità ->dati anagrafici
		 * indirizzo, recapito telefonico personale (non obbligatori)
		 * email
		 * specializzazionei/esperienze (...)
		 * lingue parlate
		 * tipo patente di guida e se automunito
		 * 
		 */
		
		/*lavoratore->disponibilità->zona
		 * periodi
		 * zone (comuni)		 * 
		 */
		
		/*lavoratore->urgenza->persona
		 * nome,cognome,telefono,indirizzo email
		 */
		
		/*lavoratore->...->lavoro svolto
		 * periodo, nome dell'azienda, mansioni svolte, luogo di lavoro
		 * retribuzione lorda giornaliera
		 */
		//<Button fx:id="Sign in"  onAction="#controllo_credenziali" text="Sign in" GridPane.columnIndex="0" GridPane.rowIndex="2"/><!--onAction="#stampaup"-->
	}

	
}
