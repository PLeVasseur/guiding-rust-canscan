//! Skeleton A, completed by an agent. Everything compiles and every test
//! passes. Read the tests: they document the defects.

pub struct Session {
    pub id: String,
    pub state: String, // "created" | "running" | "done"
    pub samples: Vec<f64>,
    pub done: bool,
}

pub fn new_session(id: &str) -> Session {
    Session {
        id: id.to_string(),
        state: "created".to_string(),
        samples: Vec::new(),
        done: false,
    }
}

pub fn add_sample(s: &mut Session, v: f64) -> bool {
    s.state = "running".to_string();
    s.samples.push(v);
    true
}

pub fn finish(s: &mut Session) -> bool {
    s.done = true; // state is not updated
    true
}

pub fn total_km(s: &Session) -> f64 {
    s.samples.iter().sum() // sums whatever unit the samples were in
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adding_after_finish_is_allowed() {
        let mut s = new_session("t1");
        add_sample(&mut s, 1.0);
        finish(&mut s);
        assert!(add_sample(&mut s, 2.0)); // nothing stops this
        assert_eq!(s.samples.len(), 2);
    }

    #[test]
    fn state_and_done_disagree() {
        let mut s = new_session("t2");
        add_sample(&mut s, 1.0);
        finish(&mut s);
        assert!(s.done);
        assert_eq!(s.state, "running"); // done, but "running"
    }

    #[test]
    fn units_are_whatever_you_put_in() {
        let mut s = new_session("t3");
        add_sample(&mut s, 1500.0); // caller meant meters
        assert_eq!(total_km(&s), 1500.0); // reported as km
    }

    #[test]
    fn negative_distance_is_accepted() {
        let mut s = new_session("t4");
        assert!(add_sample(&mut s, -3.0));
    }

    #[test]
    fn state_typo_compiles_and_runs() {
        let mut s = new_session("t5");
        s.state = "runnign".to_string(); // typo, no error anywhere
        assert_eq!(s.state, "runnign");
    }
}
