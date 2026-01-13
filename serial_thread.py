import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtSerialPort as qtsp

from typing import Optional
from queue import Queue


class SerialThread(qtc.QThread):
    receivedData = qtc.pyqtSignal(str)
    error = qtc.pyqtSignal(str)

    def __init__(self, parent: Optional[qtw.QWidget] = None):
        super().__init__(parent)

        self.serialPort = qtsp.QSerialPort()
        self.running = False
        self.writeQueue = Queue()

    def setupPortConfig(self, portName: str, baudRate: int, dataBits: qtsp.QSerialPort.DataBits, parity: qtsp.QSerialPort.Parity, stopBits: qtsp.QSerialPort.StopBits, flowControl: qtsp.QSerialPort.FlowControl) -> None:
        # https://www.ibm.com/docs/en/aix/7.3.0?topic=communication-serial-parameters
        
        self.serialPort.setPortName(portName)
        self.serialPort.setBaudRate(baudRate)
        self.serialPort.setDataBits(dataBits)
        self.serialPort.setParity(parity)
        self.serialPort.setStopBits(stopBits)
        self.serialPort.setFlowControl(flowControl)
    
    def run(self) -> None:
        if not self.serialPort.open(qtsp.QSerialPort.OpenModeFlag.ReadWrite):
            self.error.emit(f"Failed To Open Port: {self.serialPort.errorString()}")
            return
        
        self.running = True

        while self.running:
            # writing
            while not self.writeQueue.empty():
                self.serialPort.write(self.writeQueue.get())
                self.serialPort.flush()
            
            # reading
            if self.serialPort.waitForReadyRead(100):
                self.receivedData.emit(self.serialPort.readAll().data().decode())
        
        self.serialPort.close()
    
    def stop(self) -> None:
        self.running = False
        self.quit()
        self.wait()

    def writeData(self, data: str) -> None:
        if self.serialPort.isOpen():
            self.writeQueue.put(data.encode())
        else:
            self.error.emit("Serial Port Not Open")