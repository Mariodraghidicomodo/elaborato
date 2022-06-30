module el_ing_sw {
	requires javafx.graphics;
	requires javafx.fxml;
	requires java.sql;
	requires javafx.base;
	requires javafx.controls;
	
	opens elaborato to javafx.graphics, javafx.fxml; //aggiungere in caso di
	//cannot access class elaborato.Main (in module el_ing_sw) because module el_ing_sw does not export elaborato to module javafx.graphics
}