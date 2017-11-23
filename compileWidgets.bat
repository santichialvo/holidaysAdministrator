call pyuic windows\EmployeeWindow.ui -o scripts\employeeWindow_ui.py
call pyuic windows\LoginWindow.ui -o scripts\loginWindow_ui.py
call pyuic windows\DayRequestWindow.ui -o scripts\dayRequestWindow_ui.py
call pyuic windows\CancelRequestWindow.ui -o scripts\cancelRequestWindow_ui.py
call pyuic windows\RequestsWidget.ui -o scripts\requestsWidget_ui.py
call pyuic windows\EmployeeWidget.ui -o scripts\employeeWidget_ui.py
call pyuic windows\AdmDaysDialog.ui -o scripts\admDaysDialog_ui.py
call pyuic windows\NotificationsWidget.ui -o scripts\notificationsWidget_ui.py
call pyuic windows\FeriadosDialog.ui -o scripts\feriadosDialog_ui.py
call pyuic windows\ModificarFeriadosDialog.ui -o scripts\modificarFeriadosDialog_ui.py
call pyuic windows\RestriccionesDialog.ui -o scripts\restriccionesDialog_ui.py
call pyuic windows\AddRestrictionDialog.ui -o scripts\addRestrictionDialog_ui.py
call pyuic windows\NewPeriodDialog.ui -o scripts\newPeriodDialog_ui.py
call C:\"Program Files"\Anaconda3\Library\bin\pyrcc5     images\Resource_ha.qrc -o scripts\Resource_ha_rc.py
