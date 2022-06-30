package elaborato;

import java.net.URL;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.util.ResourceBundle;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.TextField;

public class inserimento_controller implements Initializable{
	//dati anagrafici
	@FXML
	private TextField nome_id;
	@FXML
	private TextField cognome_id;
	@FXML
	private TextField naz_id;
	@FXML
	private TextField data_n_id;
	@FXML
	private TextField luogo_id;
	@FXML
	private TextField lingua_id;
	@FXML
	private TextField email_id;
	@FXML
	private TextField telefono_id;
	@FXML
	private TextField indirizzo_id;
	@FXML
	private ChoiceBox<String> spec_id;
	ObservableList<String> specializzazioni
		= FXCollections.observableArrayList("bagnino","barman","istruttore di nuoto","viticoltore","floricoltore");
	@FXML
	private ChoiceBox<Boolean> auto_id;
	@FXML
	private ChoiceBox<String> tipo_patente_id;
	ObservableList<String> tipo_patente
	= FXCollections.observableArrayList("AM","A1","A2","A","B1","B","BE","C1","C1E","C","CE","D1","D1E","D","DE","KA","KB","CQC","CQCM","CFP","NO");
	
	
	//persona da contattare in caso d'emergenza
	@FXML
	private TextField p_nome_id;
	@FXML
	private TextField p_email_id;
	@FXML
	private TextField p_telefono_id;
	@FXML
	private TextField p_cognome_id;
	
	//disponibilità
	@FXML
	private TextField periodo_id;
	@FXML
	private TextField comune_id;
	
	@FXML
	private Button invio_dati_db;
	
	@FXML
	private void inviodati(ActionEvent event) {
		System.out.println("prova inserimento"); //dovrei fare andare questo pulsante solo se quasi tutti i campi sono pieni
		//invio i dati inseriti; dovrei anche fare dei controlli
		
		//richiesta driver
		/*Class.forName("org.postgresql.Driver");
		
		//creazione connessione; //creare una base di dati oppure usare quella dell uni
		Connection con = DriverManager.getConnection(null);
		
		//creazione prestatement; usato per la creazione di query
		
		//query dati lavoratore; potrei creare una classe a parte
		PreparedStatement pst=con.prepareStatement( //attenzione ricordarsi id_lavoratore
				"INSERT INTO lavoratore(id_lavoratore, nome, cognome, luogo_di_nascita, data_di_nascita, nazionalità, indirizzo, telefono, email, specia_esp, lingue_parlate, tipo_patente, automunito) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)");
		//potevo farlo tranquillamente anche con statement
		//inserimento dei valori e invio //potrei creare una classe per inserimento dei valori
		//pst.setInteger(0, ); //capire come viene inserito il valore id_lavoratore
		pst.setString(1, nome_id.getText());
		pst.setString(2, cognome_id.getText());
		pst.setString(3, luogo_id.getText());
		pst.setString(4, data_n_id.getText());
		pst.setString(5, naz_id.getText());
		pst.setString(6, indirizzo_id.getText());
		pst.setString(7, telefono_id.getText());
		pst.setString(8, email_id.getText());
		pst.setString(9, spec_id.getSelectionModel().getSelectedItem());
		pst.setString(10, lingua_id.getText());
		pst.setString(11, tipo_patente_id.getSelectionModel().getSelectedItem());
		pst.setBoolean(12, auto_id.getSelectionModel().getSelectedItem());
		
		pst.executeUpdate();
		
		//query zona
		PreparedStatement pst_zona=con.prepareStatement( //attenzione ricordarsi id_lavoratore; gli passo lo stesso sopra(query precedente)?? come lo sa??
				"INSERT INTO zona(periodo, comuni, lavoratore) VALUES (?,?,?)");
		//inserimento dei valori
		
		//invio
		pst_zona.executeUpdate();
		
		//query persona
		PreparedStatement pst_persona=con.prepareStatement( //attenzione ricordarsi id_lavoratore
				"INSERT INTO persona(nome, cognome, telefono, email, lavoratore) VALUES (?,?,?,?,?)");
		//inserimento dei valori
		
		//invio
		pst_persona.executeUpdate();
		
		/*
		//query lavoro_svolto; inserirlo in un controller diverso (controller_lavori_passati???)
		PreparedStatement pst_lavoro=con.prepareStatement( //attenzione ricordarsi id_lavoratore
				"INSERT INTO lavoro_svolto(periodo, nome_azienda, mansione, luogo_di_lavoro, retri_lorda_giornaliera, lavoratore) VALUES (?,?,?,?,?,?)");
		//inserimento dei valori
		
		//invio
		pst_lavoro.executeUpdate();*/
		
		
		//con.close();
	}
	
	@Override
	public void initialize(URL arg0, ResourceBundle arg1) {
		// TODO Auto-generated method stub
		spec_id.setItems(specializzazioni);
		//
		auto_id.getItems().add(true);
		auto_id.getItems().add(false);
		//
		tipo_patente_id.setItems(tipo_patente);
	}

}
