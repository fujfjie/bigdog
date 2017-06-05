# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: dbConfig.py
    :time: 2017/03/13
"""
DBINFO = [dbType, dbUser, dbUserPasswd, dbName, port, host, charSet]
SQLDICT = {
    'pushMailInfo':'''select mail_host,
                             mail_user,
                             mail_user_head,
                             mail_user_password,
                             mail_port,
                             mail_subject
                        from metadata.meta_push_mail
                       where program_name = 'bigdog'
                   ''',
    ### 0 ,1 ,2 对应 snapshot, group_id, record_day
    'JOBINFO': '''select a.job_id,
                         a.job_name,
                         a.job_path,
                         a.execute_time,
                         a.execute_day,
                         a.retry_count,
                         a.rule_name,
                         a.mail_list,
                         case when b.job_id is null then 4 else status end status
                    from metadata.bigdog_view_job_info a
                    left outer join
                         (select job_id,
                                 status
                            from (select job_id,
                                         status,
                                         case when @job_id = job_id then @rn:=@rn+1 else @rn:=1 end rn,
                                         @job_id := job_id
                                    from (select job_id,
                                                 status
                                            from metadata.bigdog_log_job_info b
                                           where b.snapshot = {0}
                                             and group_id = {1}
                                             and record_day = {2}
                                           order by job_id,
                                                    crontab_time desc,
                                                    execute_step desc
                                            ) a
                                    join
                                         (select @job_id := null, @rn := null) b
                                    on(1 = 1)
                                  ) a
                           where rn = 1
                         ) b
                    on(a.job_id = b.job_id)
                   where a.group_id = {1}
               ''',
    ### 0 对应 group_id ###
    'STARTJOBRELATION':'''select end_job_id,
                                 group_concat(a.start_job_id) job_list
                            from metadata.bigdog_view_job_rela a
                           where group_id = {0}
                           group by end_job_id
                       ''',
    ### 0 对应 group_id ###
    'JOBRELATION':'''select start_job_id,
                            group_concat(a.end_job_id) job_list
                       from metadata.bigdog_view_job_rela a
                      where group_id = {0}
                        and start_job_id is not null
                      group by start_job_id
                  ''',
    ### 0 对应 group_id ###
    'GROUPINFO':'''select a.group_name,
                          a.parallel_nums,
                          a.retry_count,
                          b.mail_list
                     from metadata.bigdog_group_info a
                     join
                          metadata.bigdog_view_group_staff_rela b
                     on(a.group_id = b.group_id)
                    where a.group_id = {0}
                ''',
    ### 0\1\2 对应 group_id\snapshot\status=4 ###
    'getTaskStatus': '''select count(*)
                          from metadata.bigdog_log_group_info d
                         where d.group_id = {0}
                           and d.snapshot = {1}
                           and d.status = {2}
                     ''',
    ### 0\1\2 对应 group_id\snapshot\status=4 ###
    'setTaskStatus': '''update metadata.bigdog_log_group_info d
                           set status = %d
                         where d.group_id = {0}
                           and d.snapshot = {1}
                           and d.status = {2}
                     ''',
    'getErrorTaskId': '''select listagg(job_id,',') within group (order by null) job_list
                           from ddz_game.etl_view_job_run_info d
                          where d.group_name = '%s'
                            and d.snapshot = '%s'
                            and d.status not in(1,2)
                      ''',
    'getErrorTaskIdRelation': '''select end_job_id,
                                        listagg(start_job_id,',') within group (order by null) job_list
                                  from ddz_game.etl_view_job_run_info d
                                  join
                                       ddz_game.etl_job_relation b
                                  on(d.job_id = b.end_job_id)
                                 where d.group_name = '%s'
                                   and d.snapshot = '%s'
                                   and d.status not in(1,2)
                                 group by end_job_id
                              '''
}

LOGSQLDICT = {
    'DELETELOG':'''delete
                     from metadata.bigdog_log_job_info
                    where snapshot = {0}
                      and group_id = {1}
                      and job_id = {2}
                      and record_day = {3}
                      and execute_step = {4}
                ''',
    'INSERTLOG':'''insert into metadata.bigdog_log_job_info(
                            group_id,
                            job_id,
                            record_day,
                            snapshot,
                            start_time,
                            status,
                            crontab_time,
                            execute_step,
                            log_path
                    )
                    values(
                            {0},
                            {1},
                            {2},
                            '{3}',
                            now(),
                            1,
                            str_to_date({4},'%Y%m%d%H%i%s'),
                            {5},
                            '{6}'
                    )
                ''',
    'UPDATELOG':'''update metadata.bigdog_log_job_info a
                      set a.end_time = now(),
                          a.status = {0},
                          a.error_code = {1}
                    where a.snapshot = {2}
                      and a.group_id = {3}
                      and a.job_id = {4}
                      and a.record_day = {5}
                      and a.execute_step = {6}
                   ''',
    'DELETEGROUPLOG':'''delete
                          from metadata.bigdog_log_group_info
                         where group_id = {0}
                           and record_day = {1}
                           and snapshot = {2}
                     ''',
    'INSERTGROUPLOG':'''insert into metadata.bigdog_log_group_info(
                              group_id,
                              record_day,
                              snapshot,
                              start_time,
                              status
                        )
                        values(
                              {0},
                              {1},
                              '{2}',
                              now(),
                              1
                        )
                     ''',
    'UPDATEGROUPLOG':'''update metadata.bigdog_log_group_info a
                           set a.status = {0},
                               a.end_time = now(),
                               a.conf_pv = {4},
                               a.real_pv = {5},
                               a.succ_pv = {6},
                               a.err_pv = {7}
                         where group_id = {1}
                           and record_day = {2}
                           and snapshot = {3}
                     ''',
    'groupRunInfo':'''select conf_pv,
                             rela_pv,
                             success_pv,
                             error_pv
                        from (select count(distinct case when status = 2 then job_id else null end) success_pv,
                                     count(distinct case when status = 3 then job_id else null end) error_pv
                                from (select job_id,
                                             status
                                        from (select job_id,
                                                     status,
                                                     case when @job_id = job_id then @rn:=@rn+1 else @rn:=1 end rn,
                                                     @job_id := job_id
                                                from (select job_id,
                                                             status
                                                        from metadata.bigdog_log_job_info b
                                                       where b.snapshot = {0}
                                                         and group_id = {1}
                                                         and record_day = {2}
                                                       order by job_id,
                                                                crontab_time desc,
                                                                execute_step desc
                                                      ) a
                                                join
                                                      (select @job_id := null, @rn := null) b
                                                on(1 = 1)
                                             ) a
                                       where rn = 1
                                      ) b
                             ) a
                        join
                             (select count(distinct d.job_id) conf_pv,
                                     count(distinct c.end_job_id) rela_pv
                                from metadata.bigdog_job_info d
                                join
                                     metadata.bigdog_job_rela c
                                on(d.job_id = c.end_job_id)
                               where group_id = {1}
                             ) b
                        on( 1 = 1 )
                   '''
}
