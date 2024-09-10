document.getElementById('filterButton').addEventListener('click', function() {
    const location = document.getElementById('location').value.toLowerCase();
    const jobType = document.getElementById('jobType').value.toLowerCase();
    const search = document.getElementById('search').value.toLowerCase();

    const jobs = document.querySelectorAll('.job-item');

    jobs.forEach(job => {
        const jobLocation = job.getAttribute('data-location').toLowerCase();
        const jobTypeAttr = job.getAttribute('data-type').toLowerCase();
        const jobTitle = job.querySelector('h2').textContent.toLowerCase();

        let locationMatch = location === '' || jobLocation === location;
        let typeMatch = jobType === '' || jobTypeAttr === jobType;
        let searchMatch = jobTitle.includes(search);

        if (locationMatch && typeMatch && searchMatch) {
            job.style.display = 'block';
        } else {
            job.style.display = 'none';
        }
    });
});
