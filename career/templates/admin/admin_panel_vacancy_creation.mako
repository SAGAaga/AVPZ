<%inherit file="../layout.mako"/>
<%!from career.models.career_models import Vacancy, VacancyStatusEnum, VacancyContractTypeEnum, VacancyJobTypeEnum %>
<%!from career.views.admin_views import VACANCY_EDIT_FIELDS, MY_ENUMS %>
% if error_message is not None:
    <script>
        alert('${error_message}');
    </script>
% endif
<!-- Include stylesheet -->
<link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">

<div class="box_row-center" style="width: 90%;">

	<div class="edit" style="border: 0; max-width: 75%;">

		<h3>ADD NEW VACANCY</h3>
		<br>
		<form id="edit_form" class="form" action="${request.route_url('admin_access_vacancy', id='-1')}" method="POST"
			onsubmit="event.preventDefault();validate_form(this);">
			<input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
			<% 
            def checke(enum):
                checked =""
                if input_data is not None:
                    if enum==input_data[field]:
                        checked='checked'
                return checked
        	%>
			% for field in Vacancy.__dict__.keys():
				% if field in VACANCY_EDIT_FIELDS.keys():
					% if VACANCY_EDIT_FIELDS[field] == "text":
						<div class="input_labeling">
							<label for="${field}">${field}</label>
							<input id="in_${field}" type="hidden" name="${field}" value="${'' if input_data is None else input_data[field]}">
							<div id="${field}">
								${'' if input_data is None else input_data[field]}
							</div>
						</div>
					% elif VACANCY_EDIT_FIELDS[field] == "radio":
						<div class="box_row">
							% for enum in MY_ENUMS[field]:
								<label for="is_${enum.value}">${enum.value}</label>
								
								<input id="is_${enum.value}" style="margin: 4px 10px 0 10px;" type="radio" name="${field}"
									value="${enum.value}" ${checke(enum)}>
							% endfor
							<label for="is_none_con">None</label>
							<input id="is_none_con" style="margin: 4px 10px 0 10px;" type="radio" name="${field}" value=""
								${'' if input_data is None else ('checked' if input_data[field] is None else '')}>
						</div>
					% elif VACANCY_EDIT_FIELDS[field] == "options":
						<select name="${field}" id="${field}">
							% for enum in MY_ENUMS[field]:
									<option value="${enum.value}" ${checke(enum)}>${enum.value}</option>
							% endfor
						</select>
					% endif
				% endif
			% endfor

			
			<br>
			<input type="submit" name="form.add" class="btn submit" value="Creat new vacancy">

		</form>
	</div>
</div>


<!-- Include the Quill library -->
<script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>


<!-- Initialize Quill editor -->
<script>
	this.title_Div = document.getElementById("title");
	this.in_title = document.getElementById("in_title");

	//Init Quill
	this.quill_title = new Quill("#title", {
		theme: 'snow'
	});

	//Bind the two containers together by listening to the on-change event
	this.quill_title.on('text-change',
		() => {
			this.in_title.value = this.title_Div.children[0].textContent;
		});
	//
	//
	//



	this.desc_Div = document.getElementById("desc");
	this.in_desc = document.getElementById("in_desc");

	//Init Quill
	this.quill_desc = new Quill("#desc", {
		theme: 'snow'
	});

	//Bind the two containers together by listening to the on-change event
	this.quill_desc.on('text-change',
		() => {
			this.in_desc.value = this.desc_Div.children[0].textContent;
		});
	//
	//
	//



	this.url_key_Div = document.getElementById("url_key");
	this.in_url_key = document.getElementById("in_url_key");

	//Init Quill
	this.quill_url_key = new Quill("#url_key", {
		theme: 'snow'
	});

	//Bind the two containers together by listening to the on-change event
	this.quill_url_key.on('text-change',
		() => {
			this.in_url_key.value = this.url_key_Div.children[0].textContent;
		});
	//
	//
	//



	this.location_Div = document.getElementById("location");
	this.in_location = document.getElementById("in_location");

	//Init Quill
	this.quill_location = new Quill("#location", {
		theme: 'snow'
	});

	//Bind the two containers together by listening to the on-change event
	this.quill_location.on('text-change',
		() => {
			this.in_location.value = this.location_Div.children[0].textContent;
		});
	//
	//
	//



	this.skills_Div = document.getElementById("skills");
	this.in_skills = document.getElementById("in_skills");

	//Init Quill
	this.quill_skills = new Quill("#skills", {
		theme: 'snow'
	});

	//Bind the two containers together by listening to the on-change event
	this.quill_skills.on('text-change',
		() => {
			this.in_skills.value = this.skills_Div.children[0].textContent;
		});
	//
	//
	//



	this.responsibilities_Div = document.getElementById("responsibilities");
	this.in_responsibilities = document.getElementById("in_responsibilities");

	//Init Quill
	this.quill_responsibilities = new Quill("#responsibilities", {
		theme: 'snow'
	});

	//Bind the two containers together by listening to the on-change event
	this.quill_responsibilities.on('text-change',
		() => {
			this.in_responsibilities.value = this.responsibilities_Div.children[0].textContent;
		});
	//
	//
	//


	function validate_form(f) {
		var flag = true
		if (this.in_title.value == "") {
			flag = false;
			alert("Title is required to be not empty")
		}
		if (this.in_desc.value == "") {
			flag = false;
			alert("Description is required to be not empty")
		}
		if (this.in_url_key.value == "") {
			flag = false;
			alert("URL key is required to be not empty")
		}
		if (flag) {
			f.submit();
		}
		return flag
	}
</script>