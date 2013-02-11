# This is a basic VCL configuration file for varnish.  See the vcl(7)
# man page for details on VCL syntax and semantics.
# 
# Default backend definition.  Set this to point to your content
# server.
# 


# nginx on 8010 
backend default {
    .host = "localhost";
    .port = "8010";
}

# uncomment and add IP's or domains, to test web site,
# all requests not coming from the list will be rejected
#acl testers {
#    "localhost";
#    "opencoesione.gov.it";
#    "79.16.2.94";
#    "79.52.231.109";
#    "95.245.58.53";
#    "89.97.124.16";
#    "37.183.19.208";
#    "2.38.30.119";
#}

# check access control list
sub vcl_recv {

    if (req.restarts == 0) {
        if (req.http.x-forwarded-for) {
            set req.http.X-Forwarded-For =
                req.http.X-Forwarded-For + ", " + client.ip;
        } else {
            set req.http.X-Forwarded-For = client.ip;
        }
    }


#  if (!(client.ip ~ testers)) {
#    error 403 "Accesso temporaneamente bloccato - server in manutenzione";
#  }
  
  if (req.request == "POST") {
    set req.backend = default;
    return(pass);
  }

  if (req.request != "GET" && req.request != "HEAD") {
    set req.backend = default;
    return(pass);
  }
  if (req.http.Expect) {
    set req.backend = default;
    return(pass);
  }
  if (req.http.Authenticate || req.http.Authorization) {
    set req.backend = default;
    return(pass);
  }


  # Do not cache computation requests
  if (req.url ~ "^/computation$" || req.url ~ "^/computation/.*$") {
      set req.backend = default;
      return (pass);
  }

  # Do not cache admin site
  if (req.url ~ "^/admin$" || req.url ~ "^/admin/.*$") {
      set req.backend = default;
      return (pass);
  }

  # all GET request are cached!
  if (req.request == "GET") {
    set req.backend = default;
    return(lookup);
  }

  if (req.request == "GET" && req.url ~ "\.(gif|jpg|jpeg|bmp|png|tiff|tif|ico|img|tga|wmf|woff|ttf|eot|svg|csv)\??$") {
    set req.backend = default;
    return(lookup);
  }

  if (req.request == "GET" && req.url ~ "^/$") {
    set req.backend = default;
    return(lookup);
  }

  if (req.request == "GET" && req.url ~ "\.(json|xml)\?.*$") {
    set req.backend = default;
    return(lookup);
  }

  if (req.request == "GET" && req.url ~ "\.(css|js)$") {
    set req.backend = default;
    return(lookup);
  }
set req.backend = default;
}

# adding diagnostics on why there was a hit/miss
sub vcl_fetch {
    if (req.url ~ "^/w00tw00t") {
        error 403 "Not permitted";
    }

    # Varnish determined the object was not cacheable
    if (beresp.ttl <= 0s) {
        set beresp.http.X-Cacheable = "NO:Not Cacheable";
    
    # You don't wish to cache content for logged in users
    } elsif (req.http.Cookie ~ "(UserID|_session)") {
        set beresp.http.X-Cacheable = "NO:Got Session";
        return(hit_for_pass);
    
    # You are respecting the Cache-Control=private header from the backend
    } elsif (beresp.http.Cache-Control ~ "private") {
        set beresp.http.X-Cacheable = "NO:Cache-Control=private";
        return(hit_for_pass);
    
    # Varnish determined the object was cacheable
    } else {
        set beresp.http.X-Cacheable = "YES";
    }

    if (req.url ~ "^/home/") {
      set beresp.ttl = 1s;
    }

    return(deliver);
}

sub vcl_deliver {
    if (resp.http.magicmarker) {
        /* Remove the magic marker */
        unset resp.http.magicmarker;

        /* By definition we have a fresh object */
        set resp.http.age = "0";
    }
}


# 
# Below is a commented-out copy of the default VCL logic.  If you
# redefine any of these subroutines, the built-in logic will be
# appended to your code.
# sub vcl_recv {
#     if (req.restarts == 0) {
# 	if (req.http.x-forwarded-for) {
# 	    set req.http.X-Forwarded-For =
# 		req.http.X-Forwarded-For + ", " + client.ip;
# 	} else {
# 	    set req.http.X-Forwarded-For = client.ip;
# 	}
#     }
#     if (req.request != "GET" &&
#       req.request != "HEAD" &&
#       req.request != "PUT" &&
#       req.request != "POST" &&
#       req.request != "TRACE" &&
#       req.request != "OPTIONS" &&
#       req.request != "DELETE") {
#         /* Non-RFC2616 or CONNECT which is weird. */
#         return (pipe);
#     }
#     if (req.request != "GET" && req.request != "HEAD") {
#         /* We only deal with GET and HEAD by default */
#         return (pass);
#     }
#     if (req.http.Authorization || req.http.Cookie) {
#         /* Not cacheable by default */
#         return (pass);
#     }
#     return (lookup);
# }
# 
# sub vcl_pipe {
#     # Note that only the first request to the backend will have
#     # X-Forwarded-For set.  If you use X-Forwarded-For and want to
#     # have it set for all requests, make sure to have:
#     # set bereq.http.connection = "close";
#     # here.  It is not set by default as it might break some broken web
#     # applications, like IIS with NTLM authentication.
#     return (pipe);
# }
# 
# sub vcl_pass {
#     return (pass);
# }
# 
# sub vcl_hash {
#     hash_data(req.url);
#     if (req.http.host) {
#         hash_data(req.http.host);
#     } else {
#         hash_data(server.ip);
#     }
#     return (hash);
# }
# 
# sub vcl_hit {
#     return (deliver);
# }
# 
# sub vcl_miss {
#     return (fetch);
# }
# 
# sub vcl_fetch {
#     if (beresp.ttl <= 0s ||
#         beresp.http.Set-Cookie ||
#         beresp.http.Vary == "*") {
# 		/*
# 		 * Mark as "Hit-For-Pass" for the next 2 minutes
# 		 */
# 		set beresp.ttl = 120 s;
# 		return (hit_for_pass);
#     }
#     return (deliver);
# }
# 
# sub vcl_deliver {
#     return (deliver);
# }
# 
# sub vcl_error {
#     set obj.http.Content-Type = "text/html; charset=utf-8";
#     set obj.http.Retry-After = "5";
#     synthetic {"
# <?xml version="1.0" encoding="utf-8"?>
# <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
#  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
# <html>
#   <head>
#     <title>"} + obj.status + " " + obj.response + {"</title>
#   </head>
#   <body>
#     <h1>Error "} + obj.status + " " + obj.response + {"</h1>
#     <p>"} + obj.response + {"</p>
#     <h3>Guru Meditation:</h3>
#     <p>XID: "} + req.xid + {"</p>
#     <hr>
#     <p>Varnish cache server</p>
#   </body>
# </html>
# "};
#     return (deliver);
# }
# 
# sub vcl_init {
# 	return (ok);
# }
# 
# sub vcl_fini {
# 	return (ok);
# }
