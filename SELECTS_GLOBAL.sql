--Remédios tomados
select doen.nome_doenca
          ,      medi.nome_medicamento
          ,      trmp.data_inicio_tratamento
          ,      redm.data_registro_diario_med data_registro
          ,      'Medicamento tomado? '|| case when redm.sta_medicamento_tomado = 0 then 'NÃO'
                                               when redm.sta_medicamento_tomado = 1 then 'SIM'
                                               else null end medicamento_tomado
          ,     redm.id_registro_diario_med 
          ,     paci.id_paciente
          from tb_mtc_trat_med_paciente trmp
          ,    tb_mtc_reg_diario_medicamento redm
          ,    tb_mtc_paciente paci
          ,    tb_mtc_doenca doen
          ,    tb_mtc_med_dosagem medo
          ,    tb_mtc_medicamento medi
          where trmp.id_paciente          = paci.id_paciente
          and   trmp.id_trat_med_paciente = redm.id_trat_med_paciente
          and   doen.id_doenca            = trmp.id_doenca
          and   medo.id_medicamento       = medi.id_medicamento
          and   medo.id_med_dosagem       = trmp.id_med_dosagem
          order by trmp.id_trat_med_paciente;

--Registros diários
select distinct paci.id_paciente
            ,      redi.data_registro 
            ,      redi.id_registro_diario
            ,      descricao_registro
            ,      case when sidi.id_registro_diario is not null then 
                        listagg(sidi.nome_sintoma||' - intensidade : '||sidi.intensidade_sintoma,' ; ')  over (partition by redi.id_registro_diario)
                        else null end sintomas
            from tb_mtc_paciente paci
            ,    tb_mtc_registro_diario redi
            ,    tb_mtc_sintoma_diario sidi
            where paci.id_paciente        = redi.id_paciente
            and   redi.id_registro_diario = sidi.id_registro_diario(+)
            group by paci.id_paciente
            ,        redi.data_registro 
            ,        redi.id_registro_diario
            ,        descricao_registro
            ,        sidi.nome_sintoma
            ,        sidi.intensidade_sintoma
            ,        sidi.id_registro_diario
            order by paci.id_paciente
            ,        redi.data_registro

--Pacientes, seus respectivos medicamentos e quantidade de dias dias em que não foram tomados esses medicamentos
select count(1)
            , nome_medicamento
            , nome_paciente
            from tb_mtc_paciente paci
            ,    tb_mtc_trat_med_paciente trme
            ,    tb_mtc_reg_diario_medicamento dime
            ,    tb_mtc_med_dosagem medo
            ,    tb_mtc_medicamento medi
            where paci.id_paciente = trme.id_paciente
            and   dime.id_trat_med_paciente = trme.id_trat_med_paciente
            and   trme.id_med_dosagem = medo.id_med_dosagem
            and   medo.id_medicamento = medi.id_medicamento
            and   dime.sta_medicamento_tomado = 0
            group by  nome_medicamento
            ,         nome_paciente
            having count(1) > 1;