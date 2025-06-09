// csrf_setup.js
document.addEventListener("DOMContentLoaded", function () {
  const token = frappe.csrf_token;
  const meta = document.createElement("meta");
  meta.name = "csrf-token";
  meta.content = token;
  document.head.appendChild(meta);
});