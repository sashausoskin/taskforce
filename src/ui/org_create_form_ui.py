# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_files/org_create_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateOrg(object):
    def setupUi(self, CreateOrg):
        CreateOrg.setObjectName("CreateOrg")
        CreateOrg.resize(480, 247)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateOrg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formTitle = QtWidgets.QLabel(CreateOrg)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.formTitle.setFont(font)
        self.formTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.formTitle.setObjectName("formTitle")
        self.verticalLayout.addWidget(self.formTitle)
        self.infoText = QtWidgets.QLabel(CreateOrg)
        self.infoText.setWordWrap(True)
        self.infoText.setObjectName("infoText")
        self.verticalLayout.addWidget(self.infoText)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setContentsMargins(-1, -1, -1, 10)
        self.formLayout.setObjectName("formLayout")
        self.nameLabel = QtWidgets.QLabel(CreateOrg)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameFill = QtWidgets.QLineEdit(CreateOrg)
        self.nameFill.setObjectName("nameFill")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.nameFill)
        self.codeLabel = QtWidgets.QLabel(CreateOrg)
        self.codeLabel.setObjectName("codeLabel")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.codeLabel)
        self.codeFill = QtWidgets.QLineEdit(CreateOrg)
        self.codeFill.setObjectName("codeFill")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.codeFill)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(CreateOrg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CreateOrg)
        self.buttonBox.rejected.connect(CreateOrg.close)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(CreateOrg)

    def retranslateUi(self, CreateOrg):
        _translate = QtCore.QCoreApplication.translate
        CreateOrg.setWindowTitle(_translate("CreateOrg", "Dialog"))
        self.formTitle.setText(_translate(
            "CreateOrg", "Create your organization"))
        self.infoText.setText(_translate(
            "CreateOrg", "Enter the required information about your organization below. The code is what the other users will use to join your organization. You will automatically be assigned as the admin of the organization."))
        self.nameLabel.setText(_translate("CreateOrg", "Name"))
        self.codeLabel.setText(_translate("CreateOrg", "Code"))
