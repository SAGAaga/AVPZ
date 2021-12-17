<%inherit file="../layout.mako"/>

<%!from career.models.career_models import ResumeStatusEnum, Resume %>
<%!from career.views.admin_views import RESUME_SORT_FIELDS, RESUME_RENAME_FOR_UNSORTABLE_FIELDS %>
% if error_message is not None:
    <script>
        alert('${error_message}');
    </script>
% endif
<div class="res_content">
    <form id="filter_form" class="form" action="${request.route_url('admin_panel_resumes')}" method="POST">
        <input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
        <input id="filter_in" type="hidden" name="${field_name}" value="${direction}">
        <input id="page_num" type="hidden">
        <div class="box_row-start">
            <div>
                <h4>Filter by status</h4>
                <select name="status_filter" id="filter_by_status" style="width: 150px;">
                    <option value="all" ${'selected' if filter_by_status=="all" else ''}>all</option>
                    % for stat in ResumeStatusEnum:
                        <option value="${stat.value}" ${'selected' if filter_by_status==stat.value else ''}>${stat.value}</option>
                    % endfor
                </select>
            </div>

        </div>
    <script>
        document.getElementById("filter_by_status").addEventListener("change", function(){
            document.getElementById("filter_form").submit();
        });
        function move_to_page(page){
          document.getElementById("page_num").name="page"
          document.getElementById("page_num").value=page
          document.getElementById("filter_form").submit();
        }
    </script>
    </form>


    % if data.item_count > 0:
    <table id="resume_data">
        <tr>
        % for field in Resume.__dict__.keys():
            % if field in RESUME_SORT_FIELDS:
                <th style="cursor: pointer;" id="th_${field}" onclick="sort_me(this,'${field}');">${field}  
                    <i class="arrow"></i>
                </th>
            % elif field in RESUME_RENAME_FOR_UNSORTABLE_FIELDS.keys():
                <th>${RESUME_RENAME_FOR_UNSORTABLE_FIELDS[field]}</th>
            % endif
        % endfor
            <th>Delete</th>
        </tr>
    <script>
        let filter_form=document.getElementById("filter_form");
        let filter_in=document.getElementById("filter_in");
        function sort_me(elm,name){
            filter_in.name=name
            sort_arrow_class=elm.children[0].classList
            if (sort_arrow_class.contains("up")){
                sort_arrow_class.remove("up")
                sort_arrow_class.add("down")
                filter_in.value="down"
            }
            else if ( sort_arrow_class.contains("down")){
                sort_arrow_class.remove("down")
                sort_arrow_class.add("up")
                filter_in.value="up"
            }
            else{
                sort_arrow_class.add("up")
                filter_in.value="up"
            }
            filter_form.submit();
        }
        
        function set_arrow(){
            document.getElementById("th_"+filter_in.name).children[0].classList.add(filter_in.value)
        }
        set_arrow();
    </script>



    % for resume in data:
        % if resume:
        <tr>
            <td>${resume.first_name}</td>    
            <td>${resume.last_name}</td>  
            <td>
                % if resume.phone:
                    <a href="tel:${resume.phone}">${resume.phone}</a> 
                % else:
                    ${resume.phone} 
                % endif    
            </td>
            <td>
                % if resume.email:
                    <a href="mailto:${resume.email}">${resume.email}</a> 
                % else:    
                    ${resume.email} 
                % endif       
            </td>
            <%
            cv=resume.cv_path
            cv_path = request.static_url(f'career:cv_storage/{cv[0]}/{cv[1]}/{cv}')
            %>

            <td><a  download href="${cv_path}">CV</a></td>  
            <td>
                % if ResumeStatusEnum:
                    <form id="edit_status_form_${resume.id}" class="form" action="${request.route_url('edit_resume', id=resume.id)}" method="POST" onsubmit="event.preventDefault();validate_form(this);">
                        <input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
                        <input type="hidden" name="_method" value="PATCH">
                        
                        <select name="status" id="select_status_${resume.id}">
                            % for stat in ResumeStatusEnum:
                                    <option value="${stat.value}" ${'selected' if resume.status==stat else ''}>${stat.value}</option>
                            % endfor
                        </select>
                        
                    </form>
                    <script>
                        document.getElementById("select_status_${resume.id}").addEventListener("change", function(){
                            document.getElementById("edit_status_form_${resume.id}").submit();
                        });
                    </script>
                % endif
            </td>   
            <td>${resume.created_date.strftime("%b %d %Y %H:%M:%S")}</td>   
            <td><a target="_blank" href="${request.route_url('vacancy', vacancy_key_url=resume.vacancy.url_key)}">Vacancy</a></td>   
            <td>
                <form class="form" action="${request.route_url('edit_resume', id=resume.id)}" method="POST">
                    <input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
                    <input type="submit" class="btn" name="form.delete" value="Delete">
                </form>
            </td>   

        </tr>
        % endif
    % endfor
    </table>
    % endif
</div>



<%
    if data.item_count > 0:
        first=""
        last=""
        if data.page==data.first_page:
            first="disabled"
        if data.page==data.last_page:
            last="disabled"
%>


% if data.item_count > 0:
    <nav class="box_row-center navigation" >
        <ul class="pagination justify-content-center pagination-lg">
            <li class="page-item ${first}">
                <a class="page-link" href="#" onclick="move_to_page(${data.first_page})" >First</a>
            </li>
            <li class="page-item ${first}">
                <a class="page-link" href="#" onclick="move_to_page(${data.previous_page})" >Previous</a>
            </li>

            <%
                bott_limit=data.page
                top_limit=data.last_page
                if bott_limit>3:
                    bott_limit-=3
                else:
                    bott_limit=1
                    
                if top_limit>data.page+3:
                    top_limit=data.page+3
            %>
            
            % for i in range(bott_limit,top_limit+1):
                <li class="page-item ${'active' if i == data.page else ''}"><a class="page-link" href="#" onclick="move_to_page(${i})">${i}</a></li>
            % endfor
            <li class="page-item ${last}">
                <a class="page-link" href="#" onclick="move_to_page(${data.next_page})" >Next</a>
            </li>
            <li class="page-item ${last}">
                <a class="page-link" href="#" onclick="move_to_page(${data.last_page})" >Last</a>
            </li>
        </ul>
    </nav>

% else:

  SORRY BUT 0 ITEMS WERE FOUND

% endif