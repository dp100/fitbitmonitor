node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        app = docker.build("fitbitmonitor")
    }

/*    stage('Test image') {
        app.inside {
            sh 'echo "Tests passed"'
        }
    }
*/
    stage('Push image') {
        docker.withRegistry('https://172.17.0.1:5000') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
}
