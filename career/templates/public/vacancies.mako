<%inherit file="../layout.mako"/>


% if data:
<div class="vac_content">
    % for vacancy in data:
        <ul>
            <li class="row_ref">
                <a href="${request.route_url('vacancy', vacancy_key_url=vacancy.url_key)}">
                <div class="box_row">
                <div class="sort_info">
                    <div class="basic_info">
                        ${vacancy.job_type.value if vacancy.job_type else ""} 
                        ${ vacancy.contract_type.value if vacancy.contract_type else ""}
                    </h5>
                    </div>
                    <div class="main_info">
                    <h3>${vacancy.title}</h3>
                    </div>
                </div>
                <div class="box_row">
                    <div class="location_info">
                    ${vacancy.location}
                    </div>
                    <div class="button_section">
                    <button class="btn">
                        Details
                    </button>
                    </div>
                </div>
                </div>
                </a>
            </li>
            </ul>
    % endfor

</div>

% else:

    SORRY BUT 0 ITEMS WERE FOUND

% endif
