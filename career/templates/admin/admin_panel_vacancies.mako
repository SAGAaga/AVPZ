<%inherit file="../layout.mako"/>
<%!from career.models.career_models import Vacancy, VacancyStatusEnum, VacancyContractTypeEnum, VacancyJobTypeEnum %>
<%!from career.views.admin_views import VACANCY_SORT_FIELDS, VACANCY_FILTER_FIELDS, MY_ENUMS, MY_ENUMS_VALIDATOR %>

<div class="vac_content">
  
  <form class="form" action="${request.route_url('admin_access_vacancy',id='-1')}" method="GET">
	<input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
	  <input type="submit" class="btn" name="form.add" value="ADD NEW VACANCY">
  </form>
  <br><br>
  <form id="filter_form" class="form" action="${request.route_url('admin_access_vacancies')}" method="POST">
	<input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
	<input id="filter_in" type="hidden" name="${field_name}" value="${direction}">
	<input id="page_num" type="hidden">

<table id="fiter_table_vacancy">
	<tr>
        % for field in Vacancy.__dict__.keys():
            % if field in VACANCY_SORT_FIELDS:
                <th style="cursor: pointer;" id="th_${field}" onclick="sort_me(this,'${field}');">Sort ${field}  
                    <i class="arrow"></i>
                </th>
            % endif
        % endfor
    </tr>
	<tr>
        % for field in Vacancy.__dict__.keys():
			<% temp_field_name = 'filter_'+field %>
            % if temp_field_name in VACANCY_FILTER_FIELDS:
                <th>Filter ${field}
					<select name="${temp_field_name}" id="${temp_field_name}" style="width: 150px;" onchange="send_me();">
						<option value="all" 
							${('selected' if filter[temp_field_name]=="all" else "") if temp_field_name in filter.keys() else "" }>all
						</option>
						% if field in MY_ENUMS.keys():
							% for enum in MY_ENUMS[field]:
								<option value="${enum.value}" 
									${('selected' if filter[temp_field_name]==enum.value else "") if temp_field_name in filter.keys() else ""}>${enum.value}
								</option>
							% endfor
						% else:
							<% 
								temp_unique_data=set()
							%>
							% for vac in data:
								% if vac not in temp_unique_data:
									<%
										temp_unique_data.add(vac)
									%>
									<option value="${vac.__dict__[field]}" 
										${('selected' if filter[temp_field_name]==vac.__dict__[field] else "") if temp_field_name in filter.keys() else ""}>${vac.__dict__[field]}
									</option>
								% endif
							% endfor
						% endif
					</select>
				</th>
            % endif
        % endfor
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
		function send_me(){
			filter_form.submit();
		}
        function set_arrow(){
            document.getElementById("th_"+filter_in.name).children[0].classList.add(filter_in.value)
        }
        set_arrow();
	</script>
</table>
</form>

% if data.item_count > 0:
<ul>
	% for vacancy in data:
		% if vacancy:
		<li class="row_ref">
			<a href="${request.route_url('admin_access_vacancy', id=vacancy.id)}">
				<div class="box_row">
					<div class="sort_info">
						<div class="basic_info">
							<h5>
								${vacancy.job_type.value if vacancy.job_type else ""} 
                        		${ vacancy.contract_type.value if vacancy.contract_type else ""}
							</h5>
						</div>
						<div class="main_info">
							<h3>${vacancy.title}</h3>
						</div>
					</div>
			</a>
			<div class="box_row">
				<div class="location_info" style="margin-right: 30px;">
					| ${vacancy.location} 
				</div>

				<div class="status" style="margin-right: 10px; font-weight: 700;">
					${vacancy.status.value}
				</div>

				<div style="margin-left: 30px;"
					| <i>${vacancy.created_date.strftime("%b %d %Y %H:%M:%S")}</i>
				</div>
				<div class="button_section box_row">
					<form class="form" action="${request.route_url('admin_access_vacancy', id=vacancy.id)}"
						method="GET">
						<input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
						<input type="submit" class="btn" name="form.edit" value="Edit">
					</form>

					<form class="form" action="${request.route_url('admin_access_vacancy', id=vacancy.id)}"
						method="POST">
						<input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
						<input type="submit" class="btn" name="form.delete" value="Delete">
					</form>
				</div>
			</div>
			</div>
		</li>
		% endif
	% endfor
</ul>
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
<nav class="box_row-center navigation">
	<ul class="pagination justify-content-center pagination-lg">
		<li class="page-item ${first}">
			<a class="page-link" href="#" onclick="move_to_page(${data.first_page})">First</a>
		</li>
		<li class="page-item ${first}">
			<a class="page-link" href="#" onclick="move_to_page(${data.previous_page})">Previous</a>
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
			% if i == data.page:
				<li class="page-item ${'active' if i == data.page else ''}">
					<a class="page-link" href="#" onclick="move_to_page(${i})">${i}</a>
				</li>
			% else:
				<li class="page-item"><a class="page-link" href="#" onclick="move_to_page(${i})">${i}</a></li>
			% endif
		% endfor
		<li class="page-item ${last}">
			<a class="page-link" href="#" onclick="move_to_page(${data.next_page})">Next</a>
		</li>
		<li class="page-item ${last}">
			<a class="page-link" href="#" onclick="move_to_page(${data.last_page})">Last</a>
		</li>
	</ul>
</nav>

% else:

SORRY BUT 0 ITEMS WERE FOUND

% endif