CREATE TABLE tb_mtc_doenca (
  id_doenca     NUMBER NOT NULL,
  nome_doenca   VARCHAR2(500) ,
  cid_doenca    VARCHAR2(30),
);


ALTER TABLE tb_mtc_doenca ADD CONSTRAINT tb_doenca_pk PRIMARY KEY ( id_doenca );

CREATE TABLE tb_mtc_forma_dosagem (
  id_tipo_dosagem        NUMBER NOT NULL,
  descricao_tipo_dosagem VARCHAR2(200)
);

ALTER TABLE tb_mtc_forma_dosagem ADD CONSTRAINT tb_forma_dosagem_pk PRIMARY KEY ( id_tipo_dosagem );

CREATE TABLE tb_mtc_med_dosagem (
  id_medicamento  NUMBER NOT NULL,
  id_tipo_dosagem NUMBER,
  id_med_dosagem  NUMBER
);

ALTER TABLE tb_mtc_med_dosagem ADD CONSTRAINT tb_mtc_med_dosagem_pk PRIMARY KEY ( id_med_dosagem );

CREATE TABLE tb_mtc_medicamento (
  id_medicamento        NUMBER NOT NULL,
  nome_medicamento      VARCHAR2(500),
  descricao_medicamento VARCHAR2(2000),
  dosagem_medicamento   NUMBER
);

ALTER TABLE tb_mtc_medicamento ADD CONSTRAINT tb_medicamento_pk PRIMARY KEY ( id_medicamento );

CREATE TABLE tb_mtc_paciente (
  id_paciente              NUMBER NOT NULL,
  nome_paciente            VARCHAR2(500),
  data_nascimento_paciente VARCHAR2(30),
  documento_paciente       VARCHAR2(11),
  email_paciente           VARCHAR2(300)
);


ALTER TABLE tb_mtc_paciente ADD CONSTRAINT tb_paciente_pk PRIMARY KEY ( id_paciente );

ALTER TABLE tb_mtc_paciente ADD CONSTRAINT tb_mtc_paciente__uk UNIQUE ( documento_paciente );

CREATE TABLE tb_mtc_reg_diario_medicamento (
  id_registro_diario_med   NUMBER NOT NULL,
  data_registro_diario_med VARCHAR2(30),
  id_trat_med_paciente     NUMBER,
  sta_medicamento_tomado   NUMBER
);


ALTER TABLE tb_mtc_reg_diario_medicamento ADD CONSTRAINT tb_registro_diario_medi_pk PRIMARY KEY ( id_registro_diario_med );

CREATE TABLE tb_mtc_registro_diario (
  id_registro_diario NUMBER NOT NULL,
  descricao_registro VARCHAR2(3000),
  id_paciente        NUMBER,
  humor              NUMBER,
  data_registro      VARCHAR2(30)
);


ALTER TABLE tb_mtc_registro_diario ADD CONSTRAINT tb_registro_diario_pk PRIMARY KEY ( id_registro_diario );

ALTER TABLE tb_mtc_registro_diario ADD CONSTRAINT tb_mtc_registro_diario_uk UNIQUE ( data_registro,
                                                                                     id_paciente );

CREATE TABLE tb_mtc_sintoma_diario (
  id_sintoma_diario   NUMBER NOT NULL,
  intensidade_sintoma NUMBER,
  duracao_sintoma     VARCHAR2(10),
  id_registro_diario  NUMBER,
  id_sintoma          NUMBER,
  nome_sintoma        VARCHAR2(300)
);


ALTER TABLE tb_mtc_sintoma_diario ADD CONSTRAINT tb_sintoma_diario_pk PRIMARY KEY ( id_sintoma_diario );

CREATE TABLE tb_mtc_trat_med_paciente (
  id_trat_med_paciente    NUMBER NOT NULL,
  quantidade_medicamento  NUMBER,
  data_inicio_tratamento  VARCHAR2(30),
  id_doenca               NUMBER,
  id_paciente             NUMBER,
  tratamento_ativo        NUMBER,
  data_termino_tratamento VARCHAR2(30),
  id_med_dosagem          NUMBER
);



ALTER TABLE tb_mtc_trat_med_paciente ADD CONSTRAINT tb_trat_med_paciente_pk PRIMARY KEY ( id_trat_med_paciente );

ALTER TABLE tb_mtc_med_dosagem
  ADD CONSTRAINT tb_mtc_med_dos_id_forma_dos_fk FOREIGN KEY ( id_tipo_dosagem )
    REFERENCES tb_mtc_forma_dosagem ( id_tipo_dosagem );

ALTER TABLE tb_mtc_med_dosagem
  ADD CONSTRAINT tb_mtc_med_dos_id_mtc_med_fk FOREIGN KEY ( id_medicamento )
    REFERENCES tb_mtc_medicamento ( id_medicamento );

ALTER TABLE tb_mtc_registro_diario
  ADD CONSTRAINT tb_reg_diario_id_paciente_fk FOREIGN KEY ( id_paciente )
    REFERENCES tb_mtc_paciente ( id_paciente );

ALTER TABLE tb_mtc_reg_diario_medicamento
  ADD CONSTRAINT tb_regdiamed_id_tratmedpaci_fk FOREIGN KEY ( id_trat_med_paciente )
    REFERENCES tb_mtc_trat_med_paciente ( id_trat_med_paciente );

ALTER TABLE tb_mtc_sintoma_diario
  ADD CONSTRAINT tb_sint_dia_id_reg_diario_fk FOREIGN KEY ( id_registro_diario )
    REFERENCES tb_mtc_registro_diario ( id_registro_diario );

ALTER TABLE tb_mtc_trat_med_paciente
  ADD CONSTRAINT tb_trat_med_paci_id_doenca_fk FOREIGN KEY ( id_doenca )
    REFERENCES tb_mtc_doenca ( id_doenca );

ALTER TABLE tb_mtc_trat_med_paciente
  ADD CONSTRAINT tb_trat_med_paci_id_paci_fk FOREIGN KEY ( id_paciente )
    REFERENCES tb_mtc_paciente ( id_paciente );

ALTER TABLE tb_mtc_trat_med_paciente
  ADD CONSTRAINT tb_tratmedpac_id_mtcmeddos_fk FOREIGN KEY ( id_med_dosagem )
    REFERENCES tb_mtc_med_dosagem ( id_med_dosagem );
