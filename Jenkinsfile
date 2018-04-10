node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("fitbitmonitor")
    }

/*    stage('Test image') {
        app.inside {
            sh 'echo "Tests passed"'
        }
    }
*/
    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        docker.withRegistry('http://0.0.0.0:5000') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
}
