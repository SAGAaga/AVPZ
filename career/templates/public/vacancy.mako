<%inherit file="../layout.mako"/>
% if error_message is not None:
    <script>
        alert('${error_message}');
    </script>
% endif
% if vacancy:
<div class="box_row-center">
    <div class="vac_info">
        <h3>${vacancy.title}</h3>
        <br>
        <div class="box_row-start tag_info">
            % if vacancy.location:
            <div class="box_row-start location" >
                <img src="${request.static_url('career:static/img/location.png')}" style="width: 15px; height: 18px; margin-right: 5px;"> 
                <h5> ${vacancy.location}</h5>
            </div>
            % endif
            % if vacancy.job_type:
            <div class="box_row-start clock" >
                <img src="${request.static_url('career:static/img/clock.png')}" style="width: 15px; height: 18px; margin-right: 5px;">        
                <h5> ${vacancy.job_type.value} </h5>
            </div>
            % endif
            % if vacancy.contract_type:
            <div class="box_row-start document" >
                <img src="${request.static_url('career:static/img/document.jpg')}" style="width: 15px; height: 18px; margin-right: 5px;">      
                <h5> ${ vacancy.contract_type.value}</h5>
            </div>
            % endif
        </div>
<!-- Links to social networks hear-->
                
        <a class="twitter-share-button" href="https://twitter.com/intent/tweet">
            <img src="${request.static_url('career:static/img/tweetter-button.png')}" style="width: 20px; height: 20px; margin-right: 5px;"> 
        </a>
<!-- 
        <a href="https://www.facebook.com/dialog/share?app_id=1011019248986332&amp;display=popup&amp;href=https%3A%2F%2Fwww.childrensalon.com%2Fcareers%2Fvacancies%2Fweb-analyst" title="Facebook" data-cs="Click.newWindow">
            <img src="${request.static_url('career:static/img/facebook.png')}" style="width: 20px; height: 20px; margin-right: 5px;"> 
        </a>
 -->
        <div class="description">
            ${vacancy.desc}
        </div>

        <div class="responsibilities">
            <br>
            <b>Responsibilities:</b>
            <br>
            ${vacancy.responsibilities}

        </div>

        <div class="skills">
            <b>Skills:</b>
            <br>
            ${vacancy.skills}

        </div>
    </div>
    % if input_data is not None:
    <script>
        history.back()
    </script>
    % endif
    <div class="apply">

        <h3>Apply for this position</h3>
        <br><br>
        <form class="form" action="${request.route_url('vacancy', vacancy_key_url=request.matchdict.get('vacancy_key_url'))}" method="POST" enctype="multipart/form-data">
            <input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
            <div class="input_block">
                <div class="input_labeling">
                    <label for="first_name">First name</label>
                    <input type="text" name="first_name" 
                    value="${(input_data['first_name'] if input_data['first_name'] is not None else '') if input_data is not None else ''}" required>
                </div>

                <div class="input_labeling">
                    <label for="last_name">Last_name</label>
                    <input type="text" name="last_name" 
                        value="${(input_data['last_name'] if input_data['last_name'] is not None else '') if input_data is not None else ''}">
                </div>
            </div>

            <div class="input_block">
                <div class="input_labeling">
                    <label for="email">Email</label>
                    <input type="email" name="email" 
                        value="${(input_data['email'] if input_data['email'] is not None else '') if input_data is not None else ''}">
                </div>

                <div class="input_labeling">
                    <label for="phone">Phone number</label>
                    <!-- 066-695-2387 -->
                    <input type="tel" name="phone" placeholder="xxx-xxx-xxxx" 
                        value="${(input_data['phone'] if input_data['phone'] is not None else '') if input_data is not None else ''}">                        
                </div>
            </div>

            <div class="input_labeling">
                <label for="cv_file">Upload your CV</label>
                <!-- cv_file.upload -->
                <input type="file" id="cv_file" name="cv_file" size="10000" multiple accept=".doc, .docx, .pdf" required 
                    value="${(input_data['cv_file'] if input_data['cv_file'] is not None else '') if input_data is not None else ''}"> 
                <input type="hidden" name="cv_file.static">
                <br>
                <p>(.doc, .docx, .pdf)</p>
            </div>

            <br><br>
            <input type="submit" class="btn submit" value="Apply">

        </form>
    </div>
</div>
% endif