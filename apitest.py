import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtCore import QStringListModel
#导入designer工具生成的login模块
from UI.Ui_main import *
from units import *



class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.currentapi=None
        self.currentclass=None

        super(MyMainForm, self).__init__()
        self.setupUi(self)
            

        #从baseapi获取子类名
        self.qList = [sc.__name__ for sc in baseapi.__subclasses__()]

        #将baseapi获取的子类名，设置为列表模型
        self.allapi_listView.setModel(QStringListModel(self.qList))

        #选择产品线后显示详情
        self.allapi_listView.clicked.connect(self.allapi_listView_clicked)

        self.pushButton.clicked.connect(self.pushButton_clicked)

    
    '''向布局添加内容,传入一个api类'''
    def addcontent(self,cont):

        #遍历删除verticalLayou中的组件
        for i in reversed(range(self.verticalLayout.count())):
            widget = self.verticalLayout.itemAt(i).widget()
            self.verticalLayout.removeWidget(widget)

        #将所有成员变量转化成待输入的组件
        list1=cont.list_all_member()
        for i in list1:
            self.label = QtWidgets.QLabel(i)
            self.lineEdit = QtWidgets.QLineEdit()
            self.lineEdit.setObjectName(f"{i}_lineEdit")
        
            self.verticalLayout.addWidget(self.label)
            self.verticalLayout.addWidget(self.lineEdit)
        # 添加可伸缩的空隙
        self.verticalLayout.addStretch(1)

    def allapi_listView_clicked(self,qModelIndex):
        
        self.currentapi=self.qList[qModelIndex.row()]
        
        self.currentclass=eval(f"{self.currentapi}()")
        self.addcontent(self.currentclass)

        self.textEdit.append(f"当前选中:{self.currentapi}")

    def pushButton_clicked(self):
        self.textEdit.append(f"正在测试:{self.currentapi}")

        for i in self.currentclass.list_all_member():
            exec(f"self.currentclass.{i} = self.findChild(QtWidgets.QLineEdit, f'{i}_lineEdit').text()")

        try:
            a=self.currentclass.run()
            print(a)
            if a:
                self.textEdit.append(f"{self.currentapi}可以使用")
                for i in self.currentclass.list_all_member():
                    #print(eval(f"self.currentclass.{i}"))
                    self.textEdit.append(f"{i}:{eval(f'self.currentclass.{i}')}")
            else:
                self.textEdit.append(f"{self.currentapi}测试不通")
        except Exception as e:
            #print(e)
            self.textEdit.append(f"{self.currentapi}测试不通")
            
            


    def censys():
        pass

if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())



