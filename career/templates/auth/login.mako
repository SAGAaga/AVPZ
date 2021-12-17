<%inherit file="../layout.mako"/>

<h1>Login</h1> 

${ message }
</p>
<form action="${ url }" method="post">
<input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
<input type="hidden" name="next" value="${next_url if next_url else request.route_url('admin_access_vacancies') }">
<div class="form-group">
    <label for="login">Username</label>
    <input type="text" name="login" value="${ login }">
</div>
<div class="form-group">
    <label for="password">Password</label>
    <input type="password" name="password">
</div>
<div class="form-group">
    <button type="submit" class="btn btn-default">Log In</button>
</div>
</form>