<?php
	header("Content-type: application/json");
	
	// Details about our service
	$serviceName = 'Example';
	$serviceVersion = '1.0';
	
	
	// Our username / password to check.   For this example, it's a simple 'username' and 'password' - both are case sensitive in this case !!!
	$username = '0319';
	$password = 'D2tu4boKhB6%$o';
	$authcheck = "Basic ". base64_encode( $username .':'. $password );    // Basic Authorization ::  Basic username:password
		
		
	//Get Data
	$data = file_get_contents('php://input');

	$auth = $_SERVER['HTTP_AUTHORIZATION'];   //  We need to check the username / password passed in the call


	if( $auth != $authcheck ) {			// Check supplied username/password  matches our expectation
		
		//Generate Invalid Authentication Response
		$string = '{"SMSDirectoryData": {';
		$string.= '  "error": 403,';
		$string.= '  "result": "Authentication Failed",';
		$string.= '  "service": "Example 1.1",';
		$string.= '  "version": 1.0';
		$string.= '}}';

		
		//Display Response
		echo $string;
	}
	
	
	
	elseif( !isset( $data )) {			// Check we have some data
		
		//Generate Missing Data Response
		$string = '{"SMSDirectoryData": {';
		$string.= '  "error": 401,';
		$string.= '  "result": "No Data",';
		$string.= '  "service": "Example 1.1",';
		$string.= '  "version": 1.0';
		$string.= '}}';

		
		//Display Response
		echo $string;
	}
	
	
	
	elseif( stripos( $data, '"sync": "check"') > 0 ) {		// Check if a 'check' sync, return check response.
		
		//Generate Response to 'Check' request.  All other requests should return 'error' and 'result' only tags.
		$string = '{"SMSDirectoryData": {';
		$string.= '  "error": 0,';
		$string.= '  "result": "OK",';
		$string.= '  "service": "Example 1.1",';
		$string.= '  "version": 1.0,';
		$string.= '  "status": "Ready",';
		$string.= '  "infourl": "https://help.mydomain.nz/",';
		$string.= '  "privacystatement": "This is a placeholder privacy statement. This should state what data your service collects, why and steps you take to protect the privacy of student / staff data - especially in regards to the NZ Privacy Act of 2020",';
		$string.= '  "options": {';
		$string.= '    "ics": true,';
		$string.= '    "students": {';
		$string.= '      "details": true,';
		$string.= '      "passwords": false,';
		$string.= '      "photos": false,';
		$string.= '      "groups": false,';
		$string.= '      "awards": false,';
		$string.= '      "timetables": false,';
		$string.= '      "attendance": false,';
		$string.= '      "assessments": false,';
		$string.= '      "pastoral": false,';
		$string.= '      "learningsupport": true,';
		$string.= '      "fields": {';
		$string.= '        "required": "firstname;lastname;gender;nsn",';
		$string.= '        "optional": "username;caregivers;caregivers1;caregivers2;caregiver.name;caregiver.relationship;caregiver.mobile;caregiver.email"';
		$string.= '        }';
		$string.= '      },';
		$string.= '    "staff": {';
		$string.= '      "details": true,';
		$string.= '      "passwords": false,';
		$string.= '      "photos": false,';
		$string.= '      "timetables": false,';
		$string.= '      "fields": {';
		$string.= '        "required": "firstname;lastname;gender",';
		$string.= '        "optional": "username"';
		$string.= '        }';
		$string.= '      },';
		$string.= '    "common": {';
		$string.= '      "subjects": false,';
		$string.= '      "notices": false,';
		$string.= '      "calendar": false,';
		$string.= '      "bookings": false';
		$string.= '      }';
		$string.= '    }';
		$string.= '  }';
		$string.= '}}';

		//Display Response
		echo $string;
	}

	
	
	else {			// All other messages - store the data and return 'OK' response.
		
		
		//Write xml file
		$file = fopen('data/'.time()."_".mt_rand(1000,9999).".json", "w") or die("Unable to open file!");
		fwrite($file, $data);
		fclose($file);

		//Generate Response to all other requests.
		$string = '{"SMSDirectoryData": {';
		$string.= '  "error": 0,';
		$string.= '  "result": "OK",';
		$string.= '}';

		//Display Response
		echo $string;

	}
		
		
		
?>
